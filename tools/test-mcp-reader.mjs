/* Reader/lab DOM QA. Actual browser layout is a separate verification surface. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','mcp/assets/overview.js','mcp/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,14);assert.equal(home.querySelectorAll('a[href="mcp/index.html"]').length,1);
const {window,document}=parseHTML(await read('mcp/index.html')),q=s=>document.querySelector(s),location={hash:''};
const previous=JSON.stringify({completed:['01-statistics-definition'],notes:{'01-statistics-definition':'preserve statistics'}}),storage=new Map([['learning-notes:applied-statistics:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('mcp/assets/course-data.js',root).href);await import(new URL('mcp/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'MCP 與工具整合');assert.equal(document.querySelectorAll('.chapter-link').length,54);assert.equal(document.querySelectorAll('.module-row').length,9);assert.equal(document.querySelectorAll('.mcp-lab').length,6);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const input of document.querySelectorAll('.mcp-lab input,.mcp-lab select,.mcp-lab textarea'))assert.ok(document.querySelector(`label[for="${input.id}"]`));
assert.ok(q('.mcp-diagram[role="img"] title'));
const lab=window.MCPLab,change=id=>q(id).dispatchEvent(new Event('change')),input=id=>q(id).dispatchEvent(new Event('input'));
function choose(id,value){const select=q(id),option=[...select.querySelectorAll('option')].find(item=>item.value===value);assert.ok(option);option.selected=true;change(id);}
assert.equal(lab.validateSearch('{"query":"MCP","limit":2}').ok,true);
for(const raw of ['{','[]','null','{"query":" "}','{"query":"MCP","limit":true}','{"query":"MCP","limit":"2"}','{"query":"MCP","limit":11}','{"query":"MCP","tenant":"other"}'])assert.equal(lab.validateSearch(raw).ok,false,raw);
q('#schema-input').value='{"query":"MCP","limit":0}';q('#schema-run').click();assert.equal(q('#schema-output').dataset.status,'error');
const auth={tenant:'alpha',owner:'alpha',scopes:['tickets:read'],expired:false,action:'read'};
assert.equal(lab.authorize(auth).ok,true);assert.equal(lab.authorize({...auth,owner:'beta'}).ok,false);assert.equal(lab.authorize({...auth,action:'write'}).ok,false);assert.equal(lab.authorize({...auth,expired:true}).ok,false);
choose('#auth-owner','beta');assert.equal(q('#auth-output').dataset.status,'error');choose('#auth-owner','alpha');assert.equal(q('#auth-output').dataset.status,'ok');
q('#flow-next').click();assert.ok(q('#flow-step').textContent.includes('tools/list'));choose('#flow-era','legacy');assert.ok(q('#flow-step').textContent.includes('initialize'));q('#flow-next').click();assert.ok(q('#flow-step').textContent.includes('notifications/initialized'));
choose('#result-kind','tool-error');assert.equal(q('#result-action').dataset.status,'error');assert.ok(q('#result-action').textContent.includes('isError=true'));choose('#result-kind','empty');assert.equal(q('#result-action').dataset.status,'ok');
const flow=lab.makeApproval();assert.equal(flow.commit('k').ok,false);flow.preview();flow.approve();assert.equal(flow.commit('k').ok,true);assert.equal(flow.commit('k').ok,true);assert.equal(flow.snapshot().effects,1);assert.equal(flow.commit('other').ok,false);
const stale=lab.makeApproval();stale.preview();stale.approve();stale.change();assert.equal(stale.commit('k').ok,false);assert.equal(stale.snapshot().effects,0);
q('#approval-commit').click();assert.equal(q('#approval-output').dataset.status,'error');q('#approval-preview').click();q('#approval-review').click();q('#approval-commit').click();q('#approval-commit').click();assert.equal(JSON.parse(q('#approval-state').textContent).effects,1);
assert.equal(lab.retryPlan('write-unsafe',10,1).rows.length,1);for(const budget of [.1,1,2.5,3,10])assert.ok(lab.retryPlan('read',budget,1).spent<=budget+1e-9);
q('#retry-budget').value='0';input('#retry-budget');assert.equal(q('#retry-output').dataset.status,'error');q('#retry-budget').value='3';input('#retry-budget');assert.equal(q('#retry-output').dataset.status,'ok');
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const a of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(a.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML('<html><body>'+lesson.html+'</body></html>');
  for(const element of doc.querySelectorAll('.math-source,.math-block')){const text=element.textContent.trim(),display=element.classList.contains('math-block'),tex=display?text.slice(2,-2).trim():text.slice(1,-1);assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;}
}
assert.equal(examples,30);assert.ok(equations>=6);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(9).fill(6));
navigate('01-why-mcp');q('#complete-lesson').click();q('#lesson-notes').value='工具提案不等於執行事實。';input('#lesson-notes');navigate('07-json-rpc');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-why-mcp');assert.equal(q('#lesson-notes').value,'工具提案不等於執行事實。');assert.equal(q('#progress-count').textContent,'1 / 54');assert.equal(storage.get('learning-notes:applied-statistics:v1'),previous);
q('#open-search').click();for(const text of ['MRTR','OAuth','冪等','工單']){q('#search-input').value=text;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.mcp-lab').length,6);assert.equal(JSON.parse(q('#approval-state').textContent).effects,0);assert.equal(q('#schema-output').dataset.status,'ok');
const styleDoc=parseHTML('<html><head><style>'+await read('mcp/assets/course.css')+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>10);
export const report={syntax:'PASS',units:54,chapters:9,examples,equations,labs:'protocol, schema, results, ACL, approval/idempotency, retry budgets: PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset, menu, remount: PASS',isolation:'statistics notes preserved',limit:'DOM emulation; browser layout not verified'};
