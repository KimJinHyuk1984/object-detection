// Controller integration with fake media/DOM boundaries; this is not a browser test.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import {setTimeout as delay} from "node:timers/promises";

test("progressive playback, pause, stop/resume, complete cache, seek and source reset",async()=>{
  const html=await fs.readFile(new URL("../files/lesson-03/web/index.html",import.meta.url),"utf8");
  const ids=[...html.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const ctx=new Proxy({measureText:t=>({width:t.length*10}),createLinearGradient:()=>({addColorStop(){}})},{get:(o,k)=>o[k]||(()=>{})});
  class Element extends EventTarget{
    constructor(id="",tag="div"){super();this.id=id;this.tag=tag;this.value="";this.checked=false;this.hidden=false;this.disabled=false;this.dataset={};this.style={};this.textContent="";this.children=[];this.classList={toggle(){}};this.paused=true;this.readyState=0;this.videoWidth=960;this.videoHeight=540;this.duration=180;this._time=0;this.ended=false;}
    append(...children){this.children.push(...children);}
    setAttribute(name,value){this[name]=value;}
    getContext(){return ctx;}
    toDataURL(){return "data:image/jpeg;base64,aW1hZ2U=";}
    showModal(){this.open=true;} close(){this.open=false;}
    load(){this.readyState=2;this._time=0;queueMicrotask(()=>this.dispatchEvent(new Event("loadeddata")));}
    get currentTime(){return this._time;} set currentTime(t){this._time=t;this.ended=false;this.seeking=true;setTimeout(()=>{this.seeking=false;this.dispatchEvent(new Event("seeked"));},0);}
    play(){this.paused=false;return Promise.resolve();} pause(){this.paused=true;}
    click(){}
  }
  const elements=Object.fromEntries(ids.map(id=>[id,new Element(id)]));
  const video=elements.video;
  for(const [id,value] of Object.entries({rate:"2","batch-size":"8","input-name":"image","output-name":"predictions",threshold:"50",opacity:"28"}))elements[id].value=value;
  elements.sync.checked=true;elements.loop.checked=true;
  globalThis.document={getElementById:id=>elements[id],createElement:tag=>new Element("",tag),createTextNode:t=>t};
  globalThis.window={addEventListener(){}};
  let paint=()=>{};globalThis.requestAnimationFrame=fn=>{paint=fn;};
  const blobs=[];URL.createObjectURL=blob=>{blobs.push(blob);return "blob:test-"+blobs.length;};URL.revokeObjectURL=()=>{};
  const pending=[],calls=[];
  let automatic=false;
  const result=body=>({ok:true,json:async()=>({results:body.frames.map(f=>({index:f.index,timestamp:f.timestamp,image:{width:640,height:360},predictions:[{class:"lampg",confidence:.95,box:[10,10,20,20],points:[]}],messages:[]}))})});
  globalThis.fetch=async(url,options)=>{
    if(url==="/api/config")return {ok:true,json:async()=>({workspace:"demo-space",workflow:"demo-flow",has_key:true,input_name:"image",output_name:"predictions"})};
    const body=JSON.parse(options.body);calls.push(body);
    if(automatic)return result(body);
    return new Promise((resolve,reject)=>{
      pending.push(()=>resolve(result(body)));
      options.signal.addEventListener("abort",()=>reject(new DOMException("Stopped","AbortError")),{once:true});
    });
  };
  const until=async check=>{for(let i=0;i<1000;i++){if(check())return;await delay(2);}throw Error("timed out");};
  await import("../files/lesson-03/web/dashboard.mjs");
  await delay(0);
  const choose=async name=>{elements["video-file"].files=[{name}];elements["video-file"].dispatchEvent(new Event("change"));await until(()=>elements["analysis-status"].textContent.includes("영상 준비 완료"));};
  await choose("three-minutes.mp4");
  assert.equal(elements.analyze.disabled,false);
  const first=elements.analyze.onclick();
  await until(()=>calls.length===1);
  assert.equal(calls[0].frames.length,8);
  paint();
  assert.equal(elements.buffering.hidden,false);
  assert.equal(video.paused,true);
  pending.shift()();
  await until(()=>calls.length===2);
  paint();await delay(0);
  assert.equal(video.paused,false);
  assert.equal(elements["signal-title"].textContent,"주행");
  video.currentTime=30;await delay(2);paint();
  assert.equal(elements.buffering.hidden,false);
  assert.equal(elements["signal-title"].textContent,"분석 대기");
  elements.stop.onclick();await first;
  assert.equal(video.paused,true);
  assert.equal(elements["export"].disabled,false);
  // A late result from the stopped request must never be added.
  pending.shift()();await delay(0);
  automatic=true;
  await elements.analyze.onclick();
  assert.match(elements["analysis-status"].textContent,/전체 분석 완료/);
  const requestedAfterResume=calls.slice(2).flatMap(b=>b.frames.map(f=>f.index));
  assert.ok(requestedAfterResume.every(i=>i>=8));
  assert.equal(new Set(requestedAfterResume).size,352);
  elements["export"].onclick();
  const record=JSON.parse(await blobs.at(-1).text());
  assert.equal(record.results.length,360);
  assert.equal(record.duration,180);
  assert.ok(!Object.hasOwn(record,"api_key"));
  const requestCount=calls.length;
  video.currentTime=0;await delay(2);paint();
  assert.equal(elements["signal-title"].textContent,"주행");
  assert.equal(calls.length,requestCount);
  video._time=180;video.ended=true;
  await elements.analyze.onclick();await delay(2);paint();
  assert.equal(video.currentTime,0);
  assert.equal(calls.length,requestCount);
  await choose("replacement.mp4");paint();
  assert.equal(elements["export"].disabled,true);
  assert.equal(elements["signal-title"].textContent,"분석 대기");
  assert.equal(calls.length,requestCount);
});
