import {CLASSES,COLORS,slotAt,sampleCount,resultAt,nextBatch,visible,signalState,formatTime,demoResult} from "./perception.mjs";
const $ = id => document.getElementById(id);
const video=$("video"), overlay=$("overlay"), context=overlay.getContext("2d");
const decoder=document.createElement("video"), capture=document.createElement("canvas");
decoder.muted=true;decoder.playsInline=true;decoder.preload="auto";
video.muted=true;video.loop=true;
let sourceURL=null,fileName="",cache=new Map(),generation=0,controller=null;
let running=false,wantPlay=false,waiting=false,demo=false,demoStarted=0,demoPaused=0;
let duration=0,serverKey=false,lastRender=-1,dirty=true,lastPanelKey="",lastElapsed=0;
let activeSettings={workspace:"",workflow:"",api_key:"",input_name:"image",output_name:"predictions",rate:2,batch:8};
const selected=new Set(Object.keys(CLASSES));
for(const [key,title] of Object.entries(CLASSES)){
  const label=document.createElement("label");label.className="chip";
  const checkbox=document.createElement("input");checkbox.type="checkbox";checkbox.checked=true;checkbox.value=key;
  checkbox.addEventListener("change",()=>{checkbox.checked?selected.add(key):selected.delete(key);dirty=true;});
  label.append(checkbox,document.createTextNode(title));$("class-filters").append(label);
}
function status(text){$("analysis-status").textContent=text;}
function settingsValid(){const id=/^[A-Za-z0-9_-]{1,160}$/;return id.test(activeSettings.workspace)&&id.test(activeSettings.workflow)&&id.test(activeSettings.input_name)&&id.test(activeSettings.output_name)&&(activeSettings.api_key||serverKey);}
function updateControls(){
  $("analyze").disabled=!sourceURL||demo||running||!settingsValid();
  $("analyze").textContent=cache.size?"분석 이어하기":"분석 시작";
  $("stop").hidden=!running;$("analyze").hidden=running;
  $("connection-dot").classList.toggle("ready",!!settingsValid());
  $("connection-text").textContent=settingsValid()?"Workflow 설정 완료":"Workflow 연결 대기";
  $("snapshot").disabled=!sourceURL&&!demo;$("export").disabled=!cache.size||demo;
  $("play-toggle").disabled=!sourceURL&&!demo;
  $("play-toggle").textContent=wantPlay?"Ⅱ":"▶";
  $("play-toggle").setAttribute("aria-label",wantPlay?"일시정지":"재생");
}
function cancelAnalysis(){
  generation++;controller?.abort();controller=null;running=false;waiting=false;
  $("buffering").hidden=true;updateControls();
}
function clearResults(){
  cancelAnalysis();cache.clear();dirty=true;lastPanelKey="";
  $("analysis-progress").style.width="0%";$("analysis-coverage").style.background="";
  $("response-notice").textContent="";updateControls();
}
function resetPlayback(){wantPlay=false;video.pause();waiting=false;$("buffering").hidden=true;updateControls();}
function readSettings(){return {workspace:$("workspace").value.trim(),workflow:$("workflow").value.trim(),api_key:$("api-key").value.trim(),input_name:$("input-name").value.trim(),output_name:$("output-name").value.trim(),rate:Number($("rate").value),batch:Number($("batch-size").value)};}
$("settings-open").onclick=()=>$("settings").showModal();
$("settings-save").onclick=()=>{
  const next=readSettings();
  if(JSON.stringify(next)!==JSON.stringify(activeSettings)){resetPlayback();clearResults();activeSettings=next;status("설정을 적용했습니다. 분석 시작을 누르세요.");}
  $("settings").close();updateControls();dirty=true;
};
fetch("/api/config").then(r=>{if(!r.ok)throw Error();return r.json();}).then(config=>{
  for(const [key,id] of [["workspace","workspace"],["workflow","workflow"],["input_name","input-name"],["output_name","output-name"]])if(!$(id).value||["input-name","output-name"].includes(id))$(id).value=config[key]||"";
  serverKey=config.has_key;activeSettings=readSettings();if(serverKey)$("api-key").placeholder="서버 환경 변수의 키 사용 중";updateControls();
}).catch(()=>status("서버 연결을 확인하세요. python app.py로 실행해야 합니다."));

function waitEvent(target,name,signal,timeout=15000){
  return new Promise((resolve,reject)=>{
    let timer;
    const cleanup=()=>{clearTimeout(timer);target.removeEventListener(name,done);target.removeEventListener("error",fail);signal?.removeEventListener("abort",abort);};
    const done=()=>{cleanup();resolve();};
    const fail=()=>{cleanup();reject(Error("영상을 읽을 수 없습니다. MP4(H.264) 파일을 확인하세요."));};
    const abort=()=>{cleanup();reject(new DOMException("Stopped","AbortError"));};
    target.addEventListener(name,done,{once:true});target.addEventListener("error",fail,{once:true});
    signal?.addEventListener("abort",abort,{once:true});timer=setTimeout(fail,timeout);
    if(signal?.aborted)abort();
  });
}
$("video-file").addEventListener("change",async event=>{
  const file=event.target.files[0];if(!file)return;
  resetPlayback();clearResults();demo=false;demoPaused=0;$("demo-mark").hidden=true;
  const mine=generation;
  if(sourceURL)URL.revokeObjectURL(sourceURL);
  sourceURL=URL.createObjectURL(file);fileName=file.name;duration=0;
  $("source-name").textContent=fileName;$("empty-state").hidden=true;video.hidden=false;
  $("result-badge").textContent="LOCAL VIDEO";$("mode-pill").textContent="원본";
  const loaded=waitEvent(video,"loadeddata");const decoded=waitEvent(decoder,"loadeddata");
  video.src=sourceURL;decoder.src=sourceURL;video.preload="auto";video.load();decoder.load();
  status("영상 준비 중…");
  try{
    await Promise.all([loaded,decoded]);if(mine!==generation)return;
    if(!Number.isFinite(video.duration)||video.duration<=0)throw Error("영상 길이를 읽지 못했습니다.");
    duration=video.duration;
    overlay.width=video.videoWidth;overlay.height=video.videoHeight;
    $("video-stage").style.aspectRatio=video.videoWidth+"/"+video.videoHeight;
    $("total-time").textContent=formatTime(duration);$("seek").max=duration;$("seek").value=0;$("seek").disabled=false;
    status("영상 준비 완료 · "+formatTime(duration)+" · 원본 재생 또는 분석 시작");
    dirty=true;updateControls();
  }catch(error){if(mine!==generation)return;status(error.message);$("empty-state").hidden=false;URL.revokeObjectURL(sourceURL);sourceURL=null;updateControls();}
  event.target.value="";
});
async function captureSlot(index,signal){
  if(signal.aborted)throw new DOMException("Stopped","AbortError");
  const target=index/activeSettings.rate;
  if(Math.abs(decoder.currentTime-target)>.00001||decoder.readyState<2){
    const seeked=waitEvent(decoder,"seeked",signal);decoder.currentTime=target;await seeked;
  }
  if(signal.aborted)throw new DOMException("Stopped","AbortError");
  const factor=Math.min(1,640/Math.max(decoder.videoWidth,decoder.videoHeight));
  capture.width=Math.max(1,Math.round(decoder.videoWidth*factor));
  capture.height=Math.max(1,Math.round(decoder.videoHeight*factor));
  capture.getContext("2d").drawImage(decoder,0,0,capture.width,capture.height);
  return {index,timestamp:target,jpeg:capture.toDataURL("image/jpeg",.68).split(",")[1]};
}
function paintCoverage(){
  const total=sampleCount(duration,activeSettings.rate);
  const indices=[...cache.keys()].sort((a,b)=>a-b),ranges=[];
  let first=null,last=null;
  for(const index of indices){if(first===null){first=last=index;}else if(index===last+1){last=index;}else{ranges.push([first,last+1]);first=last=index;}}
  if(first!==null)ranges.push([first,last+1]);
  const colors=["#e4e7eb 0%"];
  for(const [a,b] of ranges){const start=a/total*100,end=b/total*100;colors.push("#e4e7eb "+start+"%","#579bed "+start+"%","#579bed "+end+"%","#e4e7eb "+end+"%");}
  colors.push("#e4e7eb 100%");$("analysis-coverage").style.background="linear-gradient(to right,"+colors.join(",")+")";
  $("analysis-progress").style.width=(cache.size/total*100)+"%";
}
async function analyze(){
  if(!sourceURL||demo||running||!duration)return;
  if(!settingsValid()){$("settings").showModal();return;}
  if(video.ended||video.currentTime>=duration)video.currentTime=0;
  const mine=++generation;controller=new AbortController();const signal=controller.signal;
  running=true;wantPlay=true;updateControls();
  try{
    while(running&&mine===generation){
      const indices=nextBatch(cache,duration,activeSettings.rate,video.currentTime,activeSettings.batch);
      if(!indices.length)break;
      status("분석 "+cache.size+" / "+sampleCount(duration,activeSettings.rate)+"장 · 다음 "+indices.length+"장 준비");
      const frames=[];
      for(const index of indices)frames.push(await captureSlot(index,signal));
      if(mine!==generation)return;
      const started=performance.now();
      status("분석 "+cache.size+" / "+sampleCount(duration,activeSettings.rate)+"장 · Roboflow 응답 대기");
      const response=await fetch("/api/infer",{method:"POST",headers:{"Content-Type":"application/json"},signal,
        body:JSON.stringify({workspace:activeSettings.workspace,workflow:activeSettings.workflow,api_key:activeSettings.api_key,input_name:activeSettings.input_name,output_name:activeSettings.output_name,frames})});
      const body=await response.json();
      if(!response.ok)throw Error(body.detail||"분석을 완료하지 못했습니다.");
      if(!Array.isArray(body.results)||body.results.length!==frames.length)throw Error("분석 응답 수가 다릅니다.");
      if(mine!==generation)return;
      for(const result of body.results)cache.set(result.index,result);
      lastElapsed=(performance.now()-started)/1000;
      status("분석 "+cache.size+" / "+sampleCount(duration,activeSettings.rate)+"장 · 최근 묶음 "+lastElapsed.toFixed(1)+"초");
      paintCoverage();dirty=true;updateControls();
      // Allow controls to respond between batches.
      await new Promise(resolve=>setTimeout(resolve,0));
    }
    if(mine!==generation)return;
    running=false;status("전체 분석 완료 · "+cache.size+"장 · 다시 재생할 때 API를 호출하지 않습니다.");
    dirty=true;updateControls();
  }catch(error){
    if(mine!==generation||error.name==="AbortError")return;
    running=false;resetPlayback();status(error.message+" 저장된 결과는 유지됩니다.");
    dirty=true;updateControls();
  }
}
$("analyze").onclick=analyze;
$("stop").onclick=()=>{cancelAnalysis();resetPlayback();status("분석 중지 · 완료된 "+cache.size+"개 결과를 보관합니다. 이어하기로 계속할 수 있습니다.");};
async function playNative(){
  try{await video.play();}catch{wantPlay=false;waiting=false;status("재생 버튼을 눌러 영상을 시작하세요.");updateControls();}
}
$("play-toggle").onclick=()=>{
  if(demo){if(wantPlay)demoPaused=(performance.now()-demoStarted)/1000;else demoStarted=performance.now()-demoPaused*1000;wantPlay=!wantPlay;}
  else{wantPlay=!wantPlay;if(!wantPlay)video.pause();else if(video.ended)video.currentTime=0;}
  dirty=true;updateControls();
};
$("seek").addEventListener("input",()=>{video.currentTime=Number($("seek").value);dirty=true;});
video.addEventListener("seeked",()=>{dirty=true;});
video.addEventListener("ended",()=>{if(!video.loop){wantPlay=false;updateControls();}});
video.addEventListener("error",()=>{if(sourceURL){resetPlayback();status("브라우저가 이 영상을 재생하지 못했습니다. MP4(H.264)를 사용하세요.");}});
$("loop").onchange=()=>{video.loop=$("loop").checked;};
$("mute").onclick=()=>{video.muted=!video.muted;$("mute").textContent=video.muted?"음소거":"소리 켜짐";$("mute").setAttribute("aria-label",video.muted?"음소거 해제":"음소거");};
$("fullscreen").onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $("video-stage").requestFullscreen();}catch{status("이 브라우저에서는 전체 화면을 사용할 수 없습니다.");}};
for(const id of ["threshold","opacity"]){$(id).oninput=()=>{$(id+"-value").textContent=$(id).value+"%";dirty=true;};}
$("sync").onchange=()=>{dirty=true;};

function drawPredictions(ctx,result,width,height){
  if(!result)return;
  const predictions=visible(result,Number($("threshold").value)/100,selected);
  const sx=width/result.image.width,sy=height/result.image.height,font=Math.max(16,Math.round(width/68));
  ctx.save();ctx.font="600 "+font+"px 'Segoe UI',sans-serif";ctx.lineWidth=Math.max(2,width/480);ctx.lineJoin="round";
  // Fill road first so masks never cover object labels.
  for(const p of predictions.filter(p=>p.class==="line")){
    ctx.beginPath();p.points.forEach(([x,y],i)=>i?ctx.lineTo(x*sx,y*sy):ctx.moveTo(x*sx,y*sy));ctx.closePath();
    ctx.globalAlpha=Number($("opacity").value)/100;ctx.fillStyle=COLORS.line;ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle=COLORS.line;ctx.stroke();
  }
  for(const p of predictions){
    const color=COLORS[p.class],box=p.box;ctx.strokeStyle=color;
    if(p.class!=="line")ctx.strokeRect(box[0]*sx,box[1]*sy,(box[2]-box[0])*sx,(box[3]-box[1])*sy);
    const label=p.class.toUpperCase()+" "+Math.round(p.confidence*100)+"%",tw=ctx.measureText(label).width+16,th=font+12;
    const anchor=p.class==="line"?p.points[0]:box;
    const x=Math.min(Math.max(0,anchor[0]*sx),Math.max(0,width-tw)),y=Math.max(0,anchor[1]*sy-th);
    ctx.fillStyle=color;ctx.fillRect(x,y,tw,th);ctx.fillStyle="#101827";ctx.fillText(label,x+8,y+font+3);
  }
  ctx.restore();
}
function drawDemo(time,result){
  const w=overlay.width,h=overlay.height,ctx=context;
  const sky=ctx.createLinearGradient(0,0,0,h);sky.addColorStop(0,"#aabfd3");sky.addColorStop(.43,"#e3e8e7");sky.addColorStop(.44,"#7e8b86");sky.addColorStop(1,"#35414c");ctx.fillStyle=sky;ctx.fillRect(0,0,w,h);
  ctx.fillStyle="#7c8991";for(let i=0;i<8;i++){ctx.fillRect(i*135,145-(i%3)*27,80,115+(i%3)*27);}
  ctx.fillStyle="#46525f";ctx.beginPath();ctx.moveTo(410,235);ctx.lineTo(575,235);ctx.lineTo(950,540);ctx.lineTo(0,540);ctx.fill();
  ctx.strokeStyle="#d7dee3";ctx.lineWidth=4;ctx.setLineDash([22,26]);ctx.lineDashOffset=-time*65;ctx.beginPath();ctx.moveTo(452,238);ctx.lineTo(155,540);ctx.moveTo(538,238);ctx.lineTo(826,540);ctx.stroke();ctx.setLineDash([]);
  const car=result.predictions.find(p=>p.class==="car").box;ctx.fillStyle="#f0f2f5";ctx.fillRect(car[0]+8,car[1]+28,96,48);ctx.fillStyle="#273c50";ctx.fillRect(car[0]+24,car[1]+8,64,27);ctx.fillStyle="#bd3448";ctx.fillRect(car[0]+12,car[1]+60,18,7);ctx.fillRect(car[2]-30,car[1]+60,18,7);
  ctx.fillStyle="#28313b";ctx.fillRect(541,169,8,90);ctx.fillRect(530,92,32,86);
  for(const [i,label] of ["lampr","lampy","lampg"].entries()){ctx.beginPath();ctx.arc(546,108+i*25,8,0,Math.PI*2);ctx.fillStyle=result.predictions.some(p=>p.class===label)?COLORS[label]:"#46505c";ctx.fill();}
}
function updatePanel(result){
  const all=(result?.predictions||[]).filter(p=>p.confidence>=Number($("threshold").value)/100);
  const state=signalState(all,!!result);
  const key=JSON.stringify([state,all.map(p=>[p.class,p.confidence]),demo,waiting,running]);
  if(key===lastPanelKey)return;lastPanelKey=key;
  $("signal-display").dataset.tone=state.tone;$("signal-title").textContent=state.title;
  $("signal-caption").textContent=state.caption;$("signal-message").textContent=state.message;
  $("signal-confidence").textContent=state.confidence===null?"—":Math.round(state.confidence*100)+"%";
  $("vehicle-count").textContent=all.filter(p=>["car","motor"].includes(p.class)).length;
  $("people-count").textContent=all.filter(p=>p.class==="people").length;
  const roads=all.filter(p=>p.class==="line");$("road-confidence").textContent=roads.length?Math.round(Math.max(...roads.map(p=>p.confidence))*100)+"%":"—";
  $("road-highlight").style.opacity=roads.length?"1":".15";
  $("mode-pill").textContent=demo?"화면 예제":result?"인식 중":waiting?"분석 대기":"원본";
  $("result-badge").textContent=demo?"DEMO":result?"MODEL RESULT":"NO RESULT";
  $("response-notice").textContent=result?.messages?.join(" ")||"";
}
function tick(){
  const time=demo?(wantPlay?(performance.now()-demoStarted)/1000:demoPaused):video.currentTime;
  const result=demo?demoResult(time):video.seeking?null:resultAt(cache,time,activeSettings.rate);
  if(!demo&&sourceURL&&wantPlay){
    const needsResult=$("sync").checked&&running&&!result;
    if(needsResult){if(!video.paused)video.pause();waiting=true;}
    else{waiting=false;if(video.paused&&!video.ended&&video.readyState>=2)playNative();}
  }else waiting=false;
  $("buffering").hidden=!waiting;
  if(dirty||time!==lastRender){
    context.clearRect(0,0,overlay.width,overlay.height);
    if(demo)drawDemo(time,result);
    drawPredictions(context,result,overlay.width,overlay.height);
    updatePanel(result);$("current-time").textContent=formatTime(time);
    if(!demo)$("seek").value=time;
    lastRender=time;dirty=false;
  }
  requestAnimationFrame(tick);
}
$("demo-start").onclick=()=>{
  resetPlayback();clearResults();demo=true;wantPlay=true;demoStarted=performance.now();demoPaused=0;
  overlay.width=960;overlay.height=540;$("video-stage").style.aspectRatio="16/9";video.hidden=true;
  $("empty-state").hidden=true;$("demo-mark").hidden=false;$("source-name").textContent="가상 도로 · 화면 예제";
  $("total-time").textContent="DEMO";$("seek").disabled=true;
  status("가상 예제 · 6초마다 신호 변경 · 실제 영상 인식 결과가 아닙니다.");dirty=true;updateControls();
};
function download(blob,name){const url=URL.createObjectURL(blob),link=document.createElement("a");link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$("export").onclick=()=>{
  const record={version:2,source:fileName,duration,analysis_rate:activeSettings.rate,workspace:activeSettings.workspace,workflow:activeSettings.workflow,results:[...cache.values()].sort((a,b)=>a.index-b.index)};
  download(new Blob([JSON.stringify(record,null,2)],{type:"application/json"}),"drive-vision-results.json");
};
$("snapshot").onclick=()=>{
  const target=document.createElement("canvas");target.width=overlay.width;target.height=overlay.height+80;
  const ctx=target.getContext("2d");ctx.fillStyle="#141c28";ctx.fillRect(0,0,target.width,target.height);
  if(!demo)ctx.drawImage(video,0,80,target.width,overlay.height);ctx.drawImage(overlay,0,80);
  ctx.fillStyle="#fff";ctx.font="24px 'Malgun Gothic',sans-serif";
  ctx.fillText((demo?"DEMO · ":"")+formatTime(demo?(wantPlay?(performance.now()-demoStarted)/1000:demoPaused):video.currentTime)+" · "+$("signal-title").textContent+" · "+$("signal-message").textContent,20,48);
  target.toBlob(blob=>{if(blob)download(blob,"drive-vision-screen.png");},"image/png");
};
window.addEventListener("beforeunload",()=>{controller?.abort();if(sourceURL)URL.revokeObjectURL(sourceURL);});
requestAnimationFrame(tick);
