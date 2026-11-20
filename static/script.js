'use strict';
const byId = id => document.getElementById(id);
const pretty = {bfs:'BFS',dfs:'DFS',ucs:'UCS',greedy:'Greedy Best-First',astar:'A*'};
let mapData = null, selectedPath = [];

async function requestJSON(url, options={}) {
  const response = await fetch(url, options);
  let json;
  try { json = await response.json(); } catch { throw Error('Server did not return valid JSON.'); }
  if (!response.ok) throw Error(json.error || `Request failed: ${response.status}`);
  return json;
}
function notify(message, bad=false) {
  byId('notice').textContent = message;
  byId('notice').classList.toggle('error', bad);
}
function setRunning(busy) {
  byId('searchBtn').disabled = busy;
  byId('compareBtn').disabled = busy;
}
function clearResults() {
  selectedPath = [];
  byId('pathResult').textContent = '—';
  byId('costResult').textContent = '—';
  byId('stepsResult').textContent = '—';
  byId('runState').textContent = 'NOT RUN';
  byId('comparison').classList.add('hidden');
  renderMap();
}
function el(name, attributes={}) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', name);
  for (const [key,value] of Object.entries(attributes)) node.setAttribute(key, String(value));
  return node;
}
function pointPositions() {
  const xs = mapData.cities.map(c=>c.x), ys=mapData.cities.map(c=>c.y);
  let minX=Math.min(...xs), maxX=Math.max(...xs), minY=Math.min(...ys), maxY=Math.max(...ys);
  const spanX=Math.max(1,maxX-minX),spanY=Math.max(1,maxY-minY),scale=Math.min(570/spanX,420/spanY);
  const w=spanX*scale,h=spanY*scale,offsetX=(700-w)/2,offsetY=(530-h)/2;
  return Object.fromEntries(mapData.cities.map(c=>[c.name,{x:offsetX+(c.x-minX)*scale,y:offsetY+(maxY-c.y)*scale}]));
}
function renderMap() {
  if (!mapData) return;
  const svg=byId('mapSvg'); svg.replaceChildren();
  const pos=pointPositions();
  const bg=el('g',{'stroke':'#23364c','stroke-width':'.7','opacity':'.45'});
  for(let x=20;x<700;x+=32)bg.append(el('line',{x1:x,y1:0,x2:x,y2:530}));
  for(let y=20;y<530;y+=32)bg.append(el('line',{x1:0,y1:y,x2:700,y2:y}));
  svg.append(bg);
  const pathEdges=new Set();
  for(let i=0;i<selectedPath.length-1;i++)pathEdges.add([selectedPath[i],selectedPath[i+1]].sort().join('|'));
  const roads=el('g');
  for(const road of mapData.roads) {
    const a=pos[road.from],b=pos[road.to];if(!a||!b)continue;
    const route=pathEdges.has([road.from,road.to].sort().join('|'));
    const line=el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:`road${route?' route':''}`});
    const title=el('title');title.textContent=`${road.from} ↔ ${road.to}: ${road.km} km`;line.append(title);roads.append(line);
    const km=el('text',{x:(a.x+b.x)/2+4,y:(a.y+b.y)/2-5,class:'km-label'});km.textContent=road.km;roads.append(km);
  }
  svg.append(roads);
  const nodes=el('g');
  for(const city of mapData.cities) {
    const p=pos[city.name],route=selectedPath.includes(city.name),group=el('g',{class:'point-group'});
    const circle=el('circle',{cx:p.x,cy:p.y,r:route?8:6,class:`point${route?' route':''}`});
    const label=el('text',{x:p.x+11,y:p.y-10,class:'city-label'});label.textContent=city.name;
    const title=el('title');title.textContent=city.name;group.append(circle,label,title);nodes.append(group);
  }
  svg.append(nodes);
}
function updateMap(data) {
  mapData=data;
  const values=data.cities.map(c=>c.name).sort((a,b)=>a.localeCompare(b));
  const prevStart=byId('start').value,prevGoal=byId('goal').value;
  for(const id of ['start','goal']) {
    byId(id).replaceChildren();
    for(const city of values){const option=document.createElement('option');option.value=city;option.textContent=city;byId(id).append(option);}
  }
  byId('start').value=values.includes(prevStart)?prevStart:(values.includes('Jenin')?'Jenin':values[0]);
  byId('goal').value=values.includes(prevGoal)?prevGoal:(values.includes('Hebron')?'Hebron':values[values.length-1]);
  if(byId('start').value===byId('goal').value && values.length>1){byId('goal').value=values.find(v=>v!==byId('start').value);}
  byId('mapTitle').textContent=data.name;
  byId('mapCount').textContent=`${data.cities.length} CITIES · ${data.roads.length} ROADS`;
  clearResults();
}
function params(){return {start:byId('start').value,goal:byId('goal').value,algorithm:byId('algorithm').value};}
function showResult(r) {
  selectedPath=r.path || [];
  byId('runState').textContent=r.status.replaceAll('_',' ').toUpperCase();
  if(r.status==='ok'){
    byId('pathResult').textContent=r.path.join(' → ');
    byId('costResult').textContent=`${r.cost} km`;
    byId('stepsResult').textContent=r.steps;
    notify(`${pretty[r.algorithm]} returned a route with ${r.path.length} cities.`);
  } else if(r.status==='no_path') {
    byId('stepsResult').textContent=r.steps;
    notify('No path exists between these cities in the current map.');
  } else {
    notify(r.message || 'Algorithm is not ready. The assigned team member must implement it.',true);
  }
  renderMap();
}
async function search() {
  setRunning(true);clearResults();
  try {
    const result=await requestJSON('/api/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(params())});
    showResult(result);
  } catch(err){notify(err.message,true);byId('runState').textContent='ERROR';}
  finally{setRunning(false);}
}
function cell(row,text,cls='') {const c=document.createElement('td');c.textContent=String(text);if(cls)c.className=cls;row.append(c);}
async function compare() {
  setRunning(true);clearResults();
  try {
    const data=await requestJSON('/api/compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(params())});
    const tbody=byId('comparisonRows');tbody.replaceChildren();
    for(const r of data.results){
      const row=document.createElement('tr');
      cell(row,pretty[r.algorithm]);
      cell(row,r.path?.length?r.path.join(' → '):'—');
      cell(row,r.cost==null?'—':`${r.cost} km`);
      cell(row,r.steps??'—');
      cell(row,r.status==='ok'?(r.optimal?'Lowest found cost':'Complete'):r.status.replaceAll('_',' '),r.optimal?'ok':'muted');
      tbody.append(row);
    }
    byId('comparison').classList.remove('hidden');
    byId('runState').textContent='COMPARE';
    const ready=data.results.filter(x=>x.status==='ok');
    if(ready.length){selectedPath=ready.reduce((a,b)=>a.cost<=b.cost?a:b).path;renderMap();}
    notify(data.all_implemented?'Comparison complete. Lowest-cost result(s) are highlighted.':'Comparison prepared. Some algorithms are not implemented yet. Lowest-cost results are only among implemented algorithms.',!data.all_implemented);
  } catch(err){notify(err.message,true);}
  finally{setRunning(false);}
}
async function uploadFile(file) {
  if(!file)return;
  const form=new FormData();form.append('file',file);
  try{const data=await requestJSON('/api/map',{method:'POST',body:form});updateMap(data);notify(`Custom map loaded: ${data.cities.length} cities, ${data.roads.length} roads.`);}
  catch(err){notify(err.message,true);}
  byId('uploadInput').value='';
}
window.addEventListener('DOMContentLoaded', async()=>{
  byId('swap').addEventListener('click',()=>{const a=byId('start').value;byId('start').value=byId('goal').value;byId('goal').value=a;clearResults();});
  byId('searchBtn').addEventListener('click',search);
  byId('compareBtn').addEventListener('click',compare);
  byId('uploadInput').addEventListener('change',e=>uploadFile(e.target.files?.[0]));
  byId('resetBtn').addEventListener('click',async()=>{try{updateMap(await requestJSON('/api/map/reset',{method:'POST'}));notify('Default West Bank map restored.');}catch(err){notify(err.message,true);}});
  for(const id of ['start','goal','algorithm'])byId(id).addEventListener('change',()=>{clearResults();notify('Ready to run the selected search.');});
  try{updateMap(await requestJSON('/api/map'));notify('Map loaded. Choose your route to begin.');}
  catch(err){notify(err.message,true);}
});
