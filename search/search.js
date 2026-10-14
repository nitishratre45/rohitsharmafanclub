(()=>{'use strict';
const form=document.getElementById('siteSearch');
const input=document.getElementById('searchQuery');
const results=document.getElementById('searchResults');
const status=document.getElementById('searchStatus');
if(!form||!input||!results||!status)return;
let index=[];
const make=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el};
const add=(category,title,summary,url)=>index.push({category,title,summary:String(summary||''),url:url||'/'});
async function read(path){const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);return r.json()}
async function init(){
 const tasks=[
  ['/data/career-stats.json','Career statistics',d=>(d.formats||[]).forEach(f=>add('Batting',f.format+' batting career',Object.entries(f).filter(([k])=>k!=='format').map(([k,v])=>k+': '+v).join(' · '),'/stats/'))],
  ['/data/bowling-stats.json','Bowling statistics',d=>(d.formats||[]).forEach(f=>add('Bowling',f.format+' bowling career',Object.entries(f).filter(([k])=>k!=='format').map(([k,v])=>k+': '+v).join(' · '),'/stats/Bowling/'))],
  ['/data/records.json','Records',d=>(d.milestones||[]).forEach(m=>add(m.category||'Record',m.title,m.description||m.date,m.source||'/records/'))],
  ['/data/matches.json','Match archive',d=>(d.matches||[]).forEach(m=>add('Match',(m.format||'Match')+' vs '+(m.opponent||'opponent')+' · '+m.date,'Rohit runs: '+m.runs+' · '+(m.result||''),m.sourceUrl||'/matches/'))],
  ['/data/news.json','News',d=>[...(d.articles||[]),...(d.items||[])].forEach(n=>add(n.category||'News',n.title,n.summary||n.publisher,n.url))],
  ['/data/photo-albums.json','Photos',d=>(d.albums||[]).forEach(a=>add('Photo',a.title,a.description,a.sourceUrl||'/photos/'))],
  ['/data/videos.json','Videos',d=>(d.sources||[]).forEach(v=>add('Video',v.title,v.description,v.url))]
 ];
 const outcomes=await Promise.all(tasks.map(async task=>{try{task[2](await read(task[0]));return true}catch(e){add('Section',task[1],'Data unavailable: '+e.message,task[0]);return false}}));
 status.textContent=index.length+' searchable items loaded. Enter a term to filter.';
 render();
}
function render(){
 const q=input.value.trim().toLowerCase();
 const list=q?index.filter(x=>(x.title+' '+x.summary+' '+x.category).toLowerCase().includes(q)):index.slice(0,12);
 results.replaceChildren();
 status.textContent=q?list.length+' result(s) for "'+input.value.trim()+'"':'Popular sections and records';
 if(!list.length)results.append(make('p','muted','No results. Try a format, opponent, year or milestone.'));
 list.slice(0,60).forEach(item=>{const card=make('article','search-result');card.append(make('span','pill',item.category),make('h2','',item.title||'Search result'),make('p','',item.summary||''));const a=make('a','','Open result ↗');a.href=item.url||'/';if(/^https?:/.test(a.href)){a.target='_blank';a.rel='noopener noreferrer'}card.append(a);results.append(card)});
}
form.addEventListener('submit',e=>{e.preventDefault();render()});
input.addEventListener('input',render);
init();
})();