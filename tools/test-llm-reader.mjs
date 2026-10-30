/* Reader unit tests in a DOM emulator, not a browser layout test. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';

const root = new URL('../',import.meta.url);
const read = file => readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','llm/assets/overview.js','llm/assets/course-data.js']) parse(await read(file),{ecmaVersion:'latest'});
const {window,document} = parseHTML(await read('llm/index.html'));
const legacy = JSON.stringify({completed:['01-mental-model'],notes:{'01-mental-model':'existing note'}});
const storage = new Map([['learning-notes:langgraph:v1',legacy]]);
const mockLocation = {hash:''};
const q = selector => document.querySelector(selector);
HTMLElement.prototype.focus = function() {};
HTMLElement.prototype.scrollIntoView = function() {};
window.scrollTo = () => {};
window.print = () => {};
q('#search-dialog').showModal = function() { this.open = true; };
q('#search-dialog').close = function() { this.open = false; };
Object.assign(globalThis,{window,document,location:mockLocation,localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)},requestAnimationFrame:fn=>fn()});
await import(new URL('llm/assets/course-data.js',root).href);
await import(new URL('llm/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
// The DOM emulator does not implement a browser's select.value semantics.
Object.defineProperty(q('#lab-effort'),'value',{value:'default',writable:true,configurable:true});
const course = window.COURSE;
assert.equal(document.querySelectorAll('.chapter-link').length,38);
assert.equal(document.querySelectorAll('.module-row').length,8);
assert.ok(document.title.includes('LLM'));
assert.equal(JSON.parse(q('#lab-request').textContent).max_output_tokens,2048);
q('#tab-gemini').click();
assert.equal(JSON.parse(q('#lab-request').textContent).generation_config.max_output_tokens,2048);
q('#tab-claude').click();
assert.equal(JSON.parse(q('#lab-request').textContent).max_tokens,2048);
q('#lab-max-tokens').value = '4096';
q('#lab-max-tokens').dispatchEvent(new Event('input'));
assert.equal(JSON.parse(q('#lab-request').textContent).max_tokens,4096);
q('#lab-effort').value = 'low';
q('#lab-effort').dispatchEvent(new Event('change'));
assert.equal(JSON.parse(q('#lab-request').textContent).output_config.effort,'low');
q('#lab-structured').checked = true;
q('#lab-structured').dispatchEvent(new Event('change'));
assert.equal(JSON.parse(q('#lab-request').textContent).output_config.format.type,'json_schema');
q('#tab-openai').click();
assert.equal(JSON.parse(q('#lab-request').textContent).reasoning.effort,'low');
assert.equal(JSON.parse(q('#lab-request').textContent).text.format.strict,true);
q('#tab-gemini').click();
assert.equal(JSON.parse(q('#lab-request').textContent).generation_config.thinking_level,'low');
assert.equal(JSON.parse(q('#lab-request').textContent).response_format.mime_type,'application/json');
assert.equal(document.querySelectorAll('.provider-tab[aria-selected="true"]').length,1);
q('#sample-top-p').value = '0.1';
q('#sample-top-p').dispatchEvent(new Event('input'));
assert.equal(document.querySelectorAll('.probability-row output')[0].textContent,'100.0%');
q('#sample-top-p').value = '1';
q('#sample-temperature').value = '2';
q('#sample-temperature').dispatchEvent(new Event('input'));
assert.ok(parseFloat(document.querySelectorAll('.probability-row output')[0].textContent)<70);

function navigate(hash) {mockLocation.hash = '#'+hash;window.dispatchEvent(new Event('hashchange'));}
let equations = 0;
for(const lesson of course.lessons) {
  navigate(lesson.id);
  assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.ok(q('.lesson-breadcrumb').textContent.includes('LLM & Agents'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  if(lesson.example) assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');
  for(const link of document.querySelectorAll('.toc-links a')) assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  const {document:doc} = parseHTML(`<html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')) {
    const text = element.textContent.trim();
    const display = element.classList.contains('math-block');
    const tex = display ? text.slice(2,-2).trim() : text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));
    equations++;
  }
}
navigate(course.lessons[0].id);
q('#complete-lesson').click();
assert.equal(q('#progress-count').textContent,'1 / 38');
q('#lesson-notes').value = '記住：工具提案不等於實際執行。';
q('#lesson-notes').dispatchEvent(new Event('input'));
navigate(course.lessons[1].id);
navigate(course.lessons[0].id);
assert.equal(q('#lesson-notes').value,'記住：工具提案不等於實際執行。');
assert.equal(storage.get('learning-notes:langgraph:v1'),legacy);
assert.equal(JSON.parse(storage.get('learning-notes:llm:v1')).completed.length,1);
q('#open-search').click();
assert.equal(q('#search-dialog').open,true);
for(const query of ['thinking','Gemini','核准']) {
  q('#search-input').value = query;
  q('#search-input').dispatchEvent(new Event('input'));
  assert.ok(document.querySelectorAll('.search-result').length>0);
}
q('#close-search').click();
assert.equal(q('#search-dialog').open,false);
q('#menu-toggle').click();
assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');
q('#sidebar-shade').click();
assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
assert.ok(equations>=5);
export const report = {syntax:'PASS',chapters:38,modules:8,equations,interactions:'PASS: provider tabs, JSON schemas, budgets, thinking, sampling, TOC, search, progress, notes, mobile menu',isolation:'LangGraph storage preserved',limit:'DOM emulation; no visual layout verification'};
