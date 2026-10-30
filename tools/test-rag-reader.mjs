/* Offline DOM-emulation checks; this does not verify actual browser layout. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';

const root=new URL('../',import.meta.url);
const read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','rag/assets/overview.js','rag/assets/course-data.js']) parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.ok(home.querySelectorAll('.subject-feature').length>=3);
assert.equal(home.querySelectorAll('a[href="rag/index.html"]').length,1);
const {window,document}=parseHTML(await read('rag/index.html'));
const previous=JSON.stringify({completed:['01-service-map'],notes:{'01-service-map':'keep this'}});
const storage=new Map([['learning-notes:llm:v1',previous]]);
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
await import(new URL('rag/assets/course-data.js',root).href+'?rag-dom');
await import(new URL('rag/assets/overview.js',root).href+'?rag-dom');
await import(new URL('assets/reader.js',root).href+'?rag-dom');
assert.equal(q('.topbar-subject').textContent,'RAG');
assert.equal(document.querySelectorAll('.chapter-link').length,42);
assert.equal(document.querySelectorAll('.module-row').length,8);
assert.ok(q('#rag-answer-text').textContent.includes('三個工作日'));
assert.ok(!q('#rag-hits').textContent.includes('999999'));
assert.ok(!q('#rag-hits').textContent.includes('1800'));
assert.ok(!q('#rag-hits').textContent.includes('三十'));

// Browser select setters are not implemented by this DOM emulator.
for(const [id,value] of [['#rag-mode','bm25'],['#rag-role','reader'],['#rag-tenant','demo'],['#metric-rank-1','X'],['#metric-rank-2','A'],['#metric-rank-3','B']]) {
  Object.defineProperty(q(id),'value',{value,writable:true,configurable:true});
}
const change=id=>q(id).dispatchEvent(new Event('change'));
const submit=()=>q('#rag-search-form').dispatchEvent(new Event('submit',{cancelable:true}));
q('#rag-query').value='薪資設定';submit();
assert.ok(!q('#rag-hits').textContent.includes('999999'));
q('#rag-role').value='hr';change('#rag-role');
assert.ok(q('#rag-hits').textContent.includes('999999'));
q('#rag-role').value='reader';change('#rag-role');
assert.ok(!q('#rag-hits').textContent.includes('999999'));
q('#rag-query').value='特休申請提前';
q('#rag-tenant').value='other';change('#rag-tenant');
assert.ok(q('#rag-answer-text').textContent.includes('三十個工作日'));
q('#rag-tenant').value='demo';change('#rag-tenant');
assert.ok(q('#rag-answer-text').textContent.includes('三個工作日'));
q('[data-query="火星基地氧氣費率"]').click();
assert.ok(q('#rag-answer-status').textContent.includes('INSUFFICIENT EVIDENCE'));
q('[data-query="出差住飯店的額度"]').click();
q('#rag-mode').value='expanded';change('#rag-mode');
assert.ok(q('#rag-variants').textContent.includes('住宿費 上限'));
assert.ok(q('#rag-hits').textContent.includes('2400'));
q('#rag-k').value='1';q('#rag-k').dispatchEvent(new Event('input'));
assert.ok(document.querySelectorAll('.rag-hit').length<=1);

const lab=window.RAGLab;
assert.equal(lab.split('abcdefgh',4,0).length,2);
assert.deepEqual(lab.split('一😀二三',2,1).map(c=>c.text),['一😀','😀二','二三']);
assert.throws(()=>lab.split('x',2,2),RangeError);
assert.equal(lab.split('',20,0).length,0);
assert.ok(lab.tokenize('VPN-403 特休').includes('vpn-403'));
const sample=[{id:'a',text:'apple apple'},{id:'b',text:'banana'}];
assert.ok(Math.abs(lab.bm25('apple',sample)[0].score-Math.log(2)*4.4/(2+1.2*(.25+.75*2/1.5)))<1e-10);
assert.equal(lab.bm25('unknown',sample).length,0);
const a={doc:sample[0],score:100},b={doc:sample[1],score:1};
assert.equal(lab.rrf([[a,b],[b]])[0].doc.id,'b');
assert.ok(Math.abs(lab.rrf([[a,a]])[0].score-1/61)<1e-10);
assert.equal(lab.metrics(['A','A','A'],{A:2,B:1},3).recall,.5);
const expected=(3/Math.log2(3)+1/Math.log2(4))/(3+1/Math.log2(3));
assert.ok(Math.abs(lab.metrics(['X','A','B'],{A:2,B:1},3).ndcg-expected)<1e-10);
q('#chunk-text').value='一二三四五六七八九十甲乙丙丁戊己庚辛壬癸';
q('#chunk-size').value='20';q('#chunk-overlap').value='0';
q('#chunk-text').dispatchEvent(new Event('input'));
assert.equal(document.querySelectorAll('.rag-chunk').length,1);
q('#chunk-text').value='<img src=x onerror=alert(1)>';
q('#chunk-text').dispatchEvent(new Event('input'));
assert.equal(q('#chunk-results').querySelectorAll('img').length,0);
q('#metric-rank-1').value='A';q('#metric-rank-2').value='B';q('#metric-rank-3').value='X';change('#metric-rank-1');
assert.equal(q('[data-metric="ndcg"]').textContent,'1.000');
q('#metric-rank-2').value='A';change('#metric-rank-2');
assert.equal(q('[data-metric="recall"]').textContent,'0.500');

function navigate(hash){mockLocation.hash='#'+hash;window.dispatchEvent(new Event('hashchange'));}
const course=window.COURSE;
let equations=0;
for(const lesson of course.lessons) {
  navigate(lesson.id);
  assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.ok(q('.lesson-breadcrumb').textContent.startsWith('RAG'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const link of document.querySelectorAll('.toc-links a')) assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example) assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');
  if(lesson.text.includes('```')) assert.ok(document.querySelectorAll('.code-shell').length>0);
  const {document:doc}=parseHTML(`<html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')) {
    const text=element.textContent.trim(),display=element.classList.contains('math-block');
    const tex=display?text.slice(2,-2).trim():text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));
    equations++;
  }
}
navigate(course.lessons[0].id);
q('#complete-lesson').click();
assert.equal(q('#progress-count').textContent,'1 / 42');
q('#lesson-notes').value='引用存在與支持主張是不同的檢查。';
q('#lesson-notes').dispatchEvent(new Event('input'));
navigate(course.lessons[1].id);navigate(course.lessons[0].id);
assert.equal(q('#lesson-notes').value,'引用存在與支持主張是不同的檢查。');
assert.equal(storage.get('learning-notes:llm:v1'),previous);
assert.equal(JSON.parse(storage.get('learning-notes:rag:v1')).completed.length,1);
q('#open-search').click();
for(const query of ['BM25','GraphRAG','權限','引用']) {
  q('#search-input').value=query;q('#search-input').dispatchEvent(new Event('input'));
  assert.ok(document.querySelectorAll('.search-result').length>0);
}
q('#close-search').click();
q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');
q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');
assert.ok(q('#rag-search-form'));
assert.equal(document.querySelectorAll('.module-row').length,8);
assert.ok(equations>=12);
export const report={syntax:'PASS',chapters:42,modules:8,equations,labs:'BM25, RRF, role/tenant filtering, Unicode chunking, metrics, escaping: PASS',reader:'TOC, examples, search, progress, notes, overview remount: PASS',isolation:'LLM storage preserved',limit:'DOM emulation; no real-browser layout verification'};
