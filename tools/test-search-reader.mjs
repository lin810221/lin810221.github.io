/* DOM/numerical reader acceptance. Does not claim real-browser layout testing. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','search/assets/overview.js','search/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,16);assert.equal(home.querySelectorAll('a[href="search/index.html"]').length,1);
const {window,document}=parseHTML(await read('search/index.html')),q=s=>document.querySelector(s),location={hash:''};
const previous=JSON.stringify({completed:['01-why-mcp'],notes:{'01-why-mcp':'preserve MCP'}}),storage=new Map([['learning-notes:mcp:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('search/assets/course-data.js',root).href);await import(new URL('search/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(document.querySelectorAll('.chapter-link').length,60);assert.equal(document.querySelectorAll('.module-row').length,10);assert.equal(document.querySelectorAll('.search-lab').length,7);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const control of document.querySelectorAll('.search-lab input,.search-lab select'))assert.ok(document.querySelector(`label[for="${control.id}"]`));
assert.ok(q('.search-diagram[role="img"] title'));
const lab=window.SearchLab,input=id=>q(id).dispatchEvent(new Event('input'));
function choose(id,value){const option=[...q(id).querySelectorAll('option')].find(item=>item.value===value);assert.ok(option);option.selected=true;q(id).dispatchEvent(new Event('change'));}
assert.deepEqual(lab.analyze('ＵＳＢ 向量資料'),['usb','向量資料']);assert.deepEqual(lab.analyze('向量資料','bigrams'),['向量','量資','資料']);
choose('#token-mode','bigrams');assert.ok(q('#token-output').textContent.includes('量資'));
assert.ok(lab.bm25('hub',1.2,0).find(r=>r.id==='B').score>lab.bm25('hub',1.2,0).find(r=>r.id==='A').score);
assert.ok(lab.bm25('hub',1.2,1).find(r=>r.id==='A').score>lab.bm25('hub',1.2,1).find(r=>r.id==='B').score);
q('#bm-k1').value='0';input('#bm-k1');assert.equal(q('#bm-ranking').dataset.status,'error');q('#bm-k1').value='1.2';input('#bm-k1');assert.equal(document.querySelectorAll('.score-row').length,3);
q('#bm-b').value='';input('#bm-b');assert.equal(q('#bm-ranking').dataset.status,'error');q('#bm-b').value='.75';input('#bm-b');assert.equal(q('#bm-ranking').dataset.status,'ok');
assert.equal(lab.filtered(3).post.length,1);assert.equal(lab.filtered(8).post.length,3);assert.deepEqual(lab.filtered(3).eligibleFirst,['A1','A2','A3']);assert.throws(()=>lab.filtered(0));
q('#filter-budget').value='8';input('#filter-budget');assert.ok(q('#filter-output').textContent.includes('（3/3）'));
const fused=lab.rrf([['A','B'],['B','C']],0);assert.equal(fused[0].id,'B');assert.ok(Math.abs(fused[0].score-1.5)<1e-12);assert.deepEqual(lab.rrf([['A'],['B']],60,[1,0]).map(r=>r.id),['A']);assert.throws(()=>lab.rrf([['A','A']]));
q('#rrf-weight').value='0';input('#rrf-weight');assert.ok(!q('#rrf-output').textContent.includes('D'));
const state=lab.lifecycle();assert.equal(state.snapshot().visible,true);state.action('update');assert.equal(state.snapshot().visible,false);state.action('replay');assert.equal(state.snapshot().visible,true);state.action('delete');state.action('old');assert.equal(state.snapshot().visible,false);state.action('replay');assert.equal(state.snapshot().index,null);
q('#life-delete').click();assert.equal(JSON.parse(q('#life-state').textContent).visible,false);q('#life-replay').click();assert.equal(JSON.parse(q('#life-state').textContent).index,null);
const cap=lab.capacity(1000000,768,8,16,2,1.3,true);assert.equal(cap.vectors,768000000);assert.equal(cap.originals,3072000000);assert.equal(cap.graph,128000000);assert.equal(cap.total,10316800000);assert.throws(()=>lab.capacity(0,768,8,16,2,1.3,true));assert.equal(lab.capacity(1,8,32,0,1,1,true).originals,0);
q('#cap-n').value='0';input('#cap-n');assert.equal(q('#cap-output').dataset.status,'error');q('#cap-n').value='1000000';input('#cap-n');assert.equal(q('#cap-output').dataset.status,'ok');
const metrics=lab.quality(['A','B','C'],['A','D','B'],[3,0,1],[10,12,13,14,50]);assert.equal(metrics.recall,2/3);assert.ok(metrics.ndcg<1&&metrics.ndcg>0);assert.ok(Math.abs(metrics.p95-42.8)<1e-9);assert.equal(lab.quality([],[],[0,0,0],[1]).recall,null);assert.equal(lab.quality([],[],[0,0,0],[1]).ndcg,null);
q('#metric-times').value='10,,';input('#metric-times');assert.equal(q('#metric-output').dataset.status,'error');q('#metric-times').value='10,20';input('#metric-times');assert.equal(q('#metric-output').dataset.status,'ok');
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);assert.ok(document.querySelectorAll('.toc-links a').length>=4);
  for(const element of document.querySelectorAll('.math-block')){const tex=element.textContent.trim().replace(/^\$\$\s*|\s*\$\$$/g,'');katex.renderToString(tex,{displayMode:true,throwOnError:true,strict:'error'});equations++;}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
}
assert.equal(examples,32);assert.equal(equations,7);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(10).fill(6));
navigate('01-scope-and-overlap');q('#complete-lesson').click();q('#lesson-notes').value='索引真值與相關性分開驗證。';input('#lesson-notes');navigate('07-inverted-index-positions');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-scope-and-overlap');assert.equal(q('#lesson-notes').value,'索引真值與相關性分開驗證。');assert.equal(q('#progress-count').textContent,'1 / 60');assert.equal(storage.get('learning-notes:mcp:v1'),previous);
q('#open-search').click();for(const text of ['HNSW','Outbox','BM25','pgvector','備份']){q('#search-input').value=text;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.search-lab').length,7);assert.equal(JSON.parse(q('#life-state').textContent).visible,true);assert.equal(q('#cap-output').dataset.status,'ok');
const css=await read('search/assets/course.css'),styleDoc=parseHTML('<html><head><style>'+css+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>20);assert.ok(!css.includes('var(--border)'));assert.ok(!css.includes('var(--surface)'));
export const report={syntax:'PASS',units:60,chapters:10,examples,equations,labs:'tokenizer, BM25, filtered candidates, RRF, revisions, capacity, metrics: PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset, menu, remount: PASS',isolation:'MCP notes preserved',limit:'DOM emulation; real-browser layout not verified'};
