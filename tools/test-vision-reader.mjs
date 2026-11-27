/* Numerical, content and reader integration QA. No browser layout claims. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','image-recognition/assets/overview.js','image-recognition/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await readFile(new URL('tools/library.json',root),'utf8')).courses).length);
assert.equal(home.querySelectorAll('a[href="image-recognition/index.html"]').length,1);
const {window,document}=parseHTML(await read('image-recognition/index.html'));
const previous=JSON.stringify({completed:['01-representations'],notes:{'01-representations':'保留既有筆記'}});
const storage=new Map([['learning-notes:deep-learning:v1',previous]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('image-recognition/assets/course-data.js',root).href);
await import(new URL('image-recognition/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=id=>q('#'+id).dispatchEvent(new Event('input'));
const select=(id,value)=>{const element=q('#'+id);for(const option of element.querySelectorAll('option'))option.selected=false;element.querySelector(`option[value="${value}"]`).selected=true;element.dispatchEvent(new Event('change'));};
const near=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<tol,`${a} vs ${b}`);
assert.equal(q('.topbar-subject').textContent,'影像辨識');
assert.equal(document.querySelectorAll('.chapter-link').length,84);
assert.equal(document.querySelectorAll('.module-row').length,14);
assert.equal(document.querySelectorAll('.cv-lab').length,8);
assert.equal(document.querySelectorAll('.cv-atlas img').length,28);
let ids=[...document.querySelectorAll('[id]')].map(e=>e.id);assert.equal(ids.length,new Set(ids).size);
for(const element of document.querySelectorAll('.cv-lab input,.cv-lab select'))assert.ok(q(`label[for="${element.id}"]`));
for(const svg of document.querySelectorAll('.cv-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));}
const lab=window.VisionLab;
near(lab.rgb(255,255,255).gray,255);near(lab.rgb(255,0,0).gray,76.245);assert.throws(()=>lab.rgb(256,0,0),RangeError);
q('#cv-r').value='255';q('#cv-g').value='0';q('#cv-b').value='0';input('cv-r');assert.ok(q('#cv-color-output').textContent.includes('#ff0000'));
near(lab.conv([0,1,4,0,2,5,0,1,4],[-1,0,1,-1,0,1,-1,0,1]),13);
assert.equal(q('#cv-conv-value').textContent,'13');select('cv-kernel','identity');assert.equal(q('#cv-conv-value').textContent,'2');select('cv-kernel','blur');near(Number(q('#cv-conv-value').textContent),17/9,1e-4);
const g=lab.geometry(37,21,64),box=[4,2,31,17];assert.notEqual(g.sx,g.sy);lab.mapBox(lab.mapBox(box,g),g,true).forEach((x,i)=>near(x,box[i]));assert.throws(()=>lab.geometry(0,100),RangeError);
q('#cv-width').value='640';q('#cv-height').value='80';input('cv-width');assert.ok(q('#cv-geometry-output').textContent.includes('256×32'));
assert.deepEqual(lab.tokens(256,256,16),{count:256,pairs:65536});select('cv-patch','8');assert.equal(q('#cv-token-count').textContent,'1024');assert.throws(()=>lab.tokens(256,255,16),RangeError);
near(lab.iou([0,0,10,10],[5,0,15,10]),1/3);near(lab.iou([0,0,1,1],[1,0,2,1]),0);assert.throws(()=>lab.iou([0,0,0,1],[0,0,1,1]),RangeError);
assert.equal(lab.nms([{box:[0,0,10,10],score:.9,label:1},{box:[0,0,10,10],score:.8,label:1},{box:[0,0,10,10],score:.7,label:2}],.5).length,2);
q('#cv-shift').value='100';input('cv-shift');assert.equal(q('#cv-iou-value').textContent,'0');assert.equal(q('#cv-nms-count').textContent,'2');q('#cv-shift').value='0';input('cv-shift');assert.equal(q('#cv-nms-count').textContent,'1');
near(lab.toyAP([true,false,true],2).ap,5/6);assert.equal(lab.toyAP([],2).ap,0);assert.throws(()=>lab.toyAP([true],0),RangeError);
near(Number(q('#cv-ap-value').textContent),5/6,1e-4);q('#cv-score').value='.85';input('cv-score');assert.equal(q('#cv-ap-value').textContent,'0.5');q('#cv-score').value='1';input('cv-score');assert.equal(q('#cv-ap-value').textContent,'0');
const metrics=lab.maskMetrics([1,1,0],[1,0,1]);near(metrics.iou,1/3);near(metrics.dice,.5);assert.equal(lab.maskMetrics([0],[0]).iou,null);
assert.ok(q('#cv-mask-output').textContent.includes('IoU 0.6'));q('#cv-pred [data-cell="6"]').click();assert.ok(q('#cv-mask-output').textContent.includes('IoU 0.8'));q('#cv-pred [data-cell="14"]').click();assert.ok(q('#cv-mask-output').textContent.includes('IoU 1'));q('#cv-mask-reset').click();assert.ok(q('#cv-mask-output').textContent.includes('IoU 0.6'));
const p=lab.temperature([3,1,0],1),soft=lab.temperature([3,1,0],3);near(p.reduce((a,b)=>a+b,0),1);assert.ok(p[0]>soft[0]);assert.equal(p.indexOf(Math.max(...p)),soft.indexOf(Math.max(...soft)));assert.throws(()=>lab.temperature([1,0],0),RangeError);
q('#cv-temperature').value='3';input('cv-temperature');assert.ok(q('#cv-confidence-output').textContent.includes('最高類別仍為0'));
for(const plot of document.querySelectorAll('.cv-plot'))assert.ok(!/NaN|Infinity/.test(plot.innerHTML));
const course=window.COURSE,allIds=new Set(course.lessons.map(l=>l.id));let equations=0,examples=0;
const used=new Set();
for(const lesson of course.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  assert.ok(q('.cv-task').textContent.includes(lesson.title));
  const figure=q('.cv-figure img');assert.ok(figure.getAttribute('alt').length>=20);used.add(figure.getAttribute('src'));
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  for(const a of document.querySelectorAll('.lesson-content a[href^="#"]')){const id=a.getAttribute('href').slice(1).split('/')[0];assert.ok(allIds.has(id)||document.getElementById(id),`${lesson.id}: broken anchor ${id}`);}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  const pageIds=[...doc.querySelectorAll('[id]')].map(x=>x.id);assert.equal(pageIds.length,new Set(pageIds).size);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){
    const text=element.textContent.trim(),display=element.classList.contains('math-block'),tex=element.getAttribute('data-tex') ?? (display?text.slice(2,-2).trim():text.slice(1,-1));
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(used.size,28);assert.equal(examples,33);assert.ok(equations>=30);
navigate('001-task-map');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 84');
q('#lesson-notes').value='先核對框的半開邊界與mask類別。';q('#lesson-notes').dispatchEvent(new Event('input'));navigate('007-color');navigate('001-task-map');assert.equal(q('#lesson-notes').value,'先核對框的半開邊界與mask類別。');
assert.equal(storage.get('learning-notes:deep-learning:v1'),previous);
q('#open-search').click();for(const term of ['IoU','COCO','255','2.15.0','群組']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.cv-lab').length,8);assert.equal(q('#cv-temperature').value,'1');assert.equal(q('#cv-conv-value').textContent,'13');assert.ok(q('#cv-mask-output').textContent.includes('IoU 0.6'));
export const report={syntax:'PASS',slug:course.slug,modules:14,units:84,figures:used.size,examples,equations,labs:'8 numerical/interaction laboratories PASS',reader:'search/notes/progress/downloads/TOC/remount PASS',isolation:'existing deep-learning notes preserved',limit:'DOM emulation; real browser layout unverified'};
