/* Development DOM checks, with local .qa/vendor modules; not browser layout QA. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';

const root=new URL('../',import.meta.url);
const read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','embedding/assets/overview.js','embedding/assets/course-data.js']) parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.ok(home.querySelectorAll('.subject-feature').length>=4);
assert.equal(home.querySelectorAll('a[href="embedding/index.html"]').length,1);
const {window,document}=parseHTML(await read('embedding/index.html'));
const priorRAG=JSON.stringify({completed:['01-what-is-rag'],notes:{'01-what-is-rag':'existing RAG note'}});
const priorLLM=JSON.stringify({completed:['01-service-map'],notes:{}});
const storage=new Map([['learning-notes:rag:v1',priorRAG],['learning-notes:llm:v1',priorLLM]]);
const mockLocation={hash:''};
const q=selector=>document.querySelector(selector);
HTMLElement.prototype.focus=function(){};
HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};
window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};
q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location:mockLocation,
  localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)},requestAnimationFrame:fn=>fn()});
await import(new URL('embedding/assets/course-data.js',root).href);
await import(new URL('embedding/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'Embedding');
assert.equal(document.querySelectorAll('.chapter-link').length,48);
assert.equal(document.querySelectorAll('.module-row').length,8);
assert.equal(document.querySelectorAll('.embedding-lab').length,4);
assert.ok(q('#geometry-ranking .embedding-rank-id').textContent.includes('A'));
assert.equal(q('#projection-true-neighbor').textContent,'A');
assert.equal(q('#projection-neighbor').textContent,'B');
Object.defineProperty(q('#geometry-metric'),'value',{value:'cosine',writable:true,configurable:true});
const input=id=>q(id).dispatchEvent(new Event('input'));
const change=id=>q(id).dispatchEvent(new Event('change'));
q('#geometry-angle').value='90';input('#geometry-angle');
assert.ok(q('#geometry-ranking .embedding-rank-id').textContent.includes('B'));
const cosineScores=q('#geometry-ranking').textContent;
q('#geometry-length').value='.5';input('#geometry-length');
assert.equal(q('#geometry-ranking').textContent,cosineScores);
q('#geometry-metric').value='dot';change('#geometry-metric');
const dotBefore=Number(q('#geometry-ranking .mono').textContent);
q('#geometry-length').value='1';input('#geometry-length');
assert.ok(Math.abs(Number(q('#geometry-ranking .mono').textContent)-2*dotBefore)<1e-6);
q('#geometry-metric').value='l2';change('#geometry-metric');
assert.ok(q('#geometry-note').textContent.includes('距離最小'));
assert.ok(!q('#geometry-plot').innerHTML.includes('NaN'));
const lab=window.EmbeddingLab;
assert.equal(lab.dot([1,2],[3,4]),11);
assert.equal(lab.norm([3,4]),5);
assert.equal(lab.distance([0,0],[3,4]),5);
assert.ok(Math.abs(lab.cosine([1,1],[2,2])-1)<1e-12);
assert.throws(()=>lab.cosine([0,0],[1,0]),RangeError);
assert.throws(()=>lab.dot([1],[1,2]),RangeError);
assert.ok(Math.abs(lab.infoNCE([0,0,0],.1).loss-Math.log(3))<1e-12);
assert.throws(()=>lab.infoNCE([1,0],0),RangeError);
q('#contrastive-positive').value='0';q('#contrastive-negative-one').value='0';q('#contrastive-negative-two').value='0';
input('#contrastive-positive');
assert.equal(q('[data-probability="0"]').textContent,'33.3%');
assert.equal(q('#contrastive-loss').textContent,Math.log(3).toFixed(4));
q('#contrastive-positive').value='.2';q('#contrastive-negative-one').value='.9';q('#contrastive-negative-two').value='.1';
q('#contrastive-temperature').value='.2';input('#contrastive-temperature');
const warmLoss=Number(q('#contrastive-loss').textContent);
q('#contrastive-temperature').value='.02';input('#contrastive-temperature');
assert.ok(Number(q('#contrastive-loss').textContent)>warmLoss);
assert.ok(q('#contrastive-note').textContent.includes('負樣本分數更高'));
assert.equal(q('[data-threshold-metric="precision"]').textContent,'66.7%');
assert.ok(q('#threshold-counts').textContent.includes('TP 2 ／ FP 1 ／ FN 1 ／ TN 2'));
q('#threshold-value').value='.85';input('#threshold-value');
assert.equal(q('[data-threshold-metric="precision"]').textContent,'100.0%');
assert.equal(q('[data-threshold-metric="recall"]').textContent,'33.3%');
q('#threshold-value').value='1';input('#threshold-value');
assert.equal(q('[data-threshold-metric="precision"]').textContent,'0.0%');
const metrics=lab.metrics([1,1,0,0],[.9,.4,.8,.1],.5);
assert.equal(metrics.tp,1);assert.equal(metrics.fp,1);assert.equal(metrics.fn,1);assert.equal(metrics.tn,1);
q('#projection-angle').value='90';input('#projection-angle');
assert.equal(q('#projection-true-neighbor').textContent,'A');
assert.equal(q('#projection-neighbor').textContent,'A');
assert.deepEqual(lab.project([1,2,3],0),[1,2]);
assert.ok(Math.abs(lab.project([1,2,3],90)[0]-3)<1e-12);

function navigate(hash){mockLocation.hash='#'+hash;window.dispatchEvent(new Event('hashchange'));}
const course=window.COURSE;
let equations=0,examples=0;
for(const lesson of course.lessons){
  navigate(lesson.id);
  assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.ok(q('.lesson-breadcrumb').textContent.startsWith('Embedding'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const link of document.querySelectorAll('.toc-links a')) assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  if(lesson.text.includes('```'))assert.ok(document.querySelectorAll('.code-shell').length>0);
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){
    const text=element.textContent.trim(),display=element.classList.contains('math-block');
    const tex=display?text.slice(2,-2).trim():text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));
    equations++;
  }
}
assert.equal(examples,20);
navigate(course.lessons[0].id);
q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 48');
q('#lesson-notes').value='同維度不表示同空間；分數不是正確率。';
q('#lesson-notes').dispatchEvent(new Event('input'));
navigate(course.lessons[1].id);navigate(course.lessons[0].id);
assert.equal(q('#lesson-notes').value,'同維度不表示同空間；分數不是正確率。');
assert.equal(storage.get('learning-notes:rag:v1'),priorRAG);
assert.equal(storage.get('learning-notes:llm:v1'),priorLLM);
assert.equal(JSON.parse(storage.get('learning-notes:embedding:v1')).completed.length,1);
q('#open-search').click();
for(const query of ['GloVe','量化','SimCSE','溫度']){q('#search-input').value=query;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();
q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');
q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.embedding-lab').length,4);
assert.equal(q('#projection-neighbor').textContent,'B');
assert.ok(equations>=27);
export const report={syntax:'PASS',chapters:48,modules:8,examples,equations,
  labs:'geometry, InfoNCE, temperature, decision metrics, projected neighbors: PASS',
  reader:'TOC, downloads, search, notes, progress, menu, remount: PASS',
  isolation:'RAG and LLM notes preserved',limit:'DOM emulation; no real-browser layout check'};
