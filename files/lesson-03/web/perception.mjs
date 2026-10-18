export const CLASSES = {car:"자동차",motor:"오토바이",people:"사람",sign:"표지판",lampg:"초록 신호",lampr:"빨간 신호",lampy:"노란 신호",lamp:"신호등",line:"주행 도로"};
export const COLORS = {car:"#63a6ff",motor:"#d69bff",people:"#ffac6e",sign:"#e4cf8c",lampg:"#53dca1",lampr:"#ff677a",lampy:"#ffdb62",lamp:"#c3ccd9",line:"#419dff"};
export const slotAt = (time, rate) => Math.max(0, Math.floor((time + 0.00001) * rate));
export const sampleCount = (duration, rate) => Math.ceil(duration * rate - 0.000001);
export function resultAt(cache, time, rate) {return cache.get(slotAt(time,rate)) || null;}
export function nextBatch(cache, duration, rate, current, size) {
  const total=sampleCount(duration,rate), start=Math.min(total-1,slotAt(current,rate));
  const order=[];
  for(let i=start;i<total && order.length<size;i++)if(!cache.has(i))order.push(i);
  for(let i=0;i<start && order.length<size;i++)if(!cache.has(i))order.push(i);
  return order;
}
export function visible(result, threshold, selected) {
  return (result?.predictions || []).filter(p => p.confidence >= threshold && selected.has(p.class));
}
export function signalState(predictions, available=true) {
  if(!available)return {tone:"neutral",title:"분석 대기",caption:"WAITING FOR ANALYSIS",message:"현재 구간의 결과를 기다립니다.",confidence:null};
  const priorities=[
    ["lampr","red","정지","RED SIGNAL","빨간 신호가 감지되었습니다."],
    ["lampy","yellow","감속","YELLOW SIGNAL","속도를 줄이고 정지를 준비하세요."],
    ["lamp","neutral","신호 확인","CHECK SIGNAL","신호등 색을 구분하기 어렵습니다."],
    ["lampg","green","주행","GREEN SIGNAL","조심히 가세요. 주변을 확인하세요."]
  ];
  for(const [label,tone,title,caption,message] of priorities){
    const matches=predictions.filter(p=>p.class===label);
    if(matches.length)return {tone,title,caption,message,confidence:Math.max(...matches.map(p=>p.confidence))};
  }
  return {tone:"neutral",title:"신호 확인",caption:"SIGNAL NOT DETECTED",message:"인식된 신호등이 없습니다.",confidence:null};
}
export function formatTime(value){const s=Math.max(0,Math.floor(value||0));return Math.floor(s/60).toString().padStart(2,"0")+":"+(s%60).toString().padStart(2,"0");}
export function demoResult(time){
  const phase=Math.floor(time/6)%4, label=["lampg","lampy","lampr","lamp"][phase];
  const shift=Math.sin(time*.7)*25;
  return {image:{width:960,height:540},predictions:[
    {class:"line",confidence:.94,box:[200,225,840,539],points:[[450,235],[545,235],[830,535],[150,535]]},
    {class:"car",confidence:.92,box:[360+shift,268,472+shift,350],points:[]},
    {class:"motor",confidence:.84,box:[630-shift,310,670-shift,372],points:[]},
    {class:label,confidence:.96,box:[533,95,560,174],points:[]}
  ],messages:[]};
}
