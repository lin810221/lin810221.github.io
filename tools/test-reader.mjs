/* DOM-emulation unit checks. This does not replace a real-browser visual review. */
import { readFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
import { parseHTML, Event, HTMLElement } from '../.qa/vendor/linkedom.mjs';
import { parse } from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';

const root = new URL('../', import.meta.url);
const read = file => readFile(new URL(file, root), 'utf8');
const dataScript = await read('langgraph/assets/course-data.js');
const appScript = await read('assets/reader.js');
parse(dataScript, {ecmaVersion: 'latest'});
parse(appScript, {ecmaVersion: 'latest'});
const { window, document } = parseHTML(await read('langgraph/index.html'));
const storage = new Map();
const mockLocation = {hash: ''};
const q = selector => document.querySelector(selector);
HTMLElement.prototype.focus = function () {};
HTMLElement.prototype.scrollIntoView = function () {};
window.scrollTo = () => {};
window.print = () => {};
const dialog = q('#search-dialog');
dialog.showModal = function () { this.open = true; };
dialog.close = function () { this.open = false; };
Object.assign(globalThis, {
  window, document, location: mockLocation,
  localStorage: {getItem:key => storage.get(key) ?? null, setItem:(key,value) => storage.set(key,value)},
  requestAnimationFrame: callback => callback(),
});

await import(new URL('langgraph/assets/course-data.js', root).href);
await import(new URL('assets/reader.js', root).href);
assert.equal(document.querySelectorAll('.chapter-link').length, 28);
assert.equal(document.querySelectorAll('.module-row').length, 6);
assert.equal(document.querySelectorAll('.graph-node').length, 6);
assert.equal(q('#lab-counter').textContent, 'STEP 01 / 06');
for (let index = 0; index < 5; index++) q('#lab-next').click();
assert.equal(q('#lab-counter').textContent, 'STEP 06 / 06');
assert.equal(q('#lab-next').disabled, true);
q('#lab-reset').click();
assert.equal(q('#lab-counter').textContent, 'STEP 01 / 06');

function navigate(hash) {
  mockLocation.hash = '#' + hash;
  window.dispatchEvent(new Event('hashchange'));
}
const course = window.COURSE;
for (const lesson of course.lessons) {
  navigate(lesson.id);
  assert.equal(q('.lesson-header h1').textContent, lesson.title);
  assert.ok(document.querySelectorAll('.toc-links a').length >= 4);
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length, 1);
  assert.ok(document.querySelectorAll('.code-shell').length >= 1 || !lesson.text.includes('```'));
  for (const link of document.querySelectorAll('.toc-links a')) {
    const id = link.getAttribute('href').split('/')[1];
    assert.ok(document.getElementById(id), `Missing TOC target: ${id}`);
  }
}

navigate(course.lessons[0].id);
q('#complete-lesson').click();
assert.equal(q('#progress-count').textContent, '1 / 28');
assert.equal(q('#complete-lesson').getAttribute('aria-pressed'), 'true');
q('#lesson-notes').value = '自己的理解：State 是資料契約。';
q('#lesson-notes').dispatchEvent(new Event('input'));
navigate(course.lessons[1].id);
navigate(course.lessons[0].id);
assert.equal(q('#lesson-notes').value, '自己的理解：State 是資料契約。');
assert.ok(JSON.parse(storage.get('learning-notes:langgraph:v1')).completed.includes(course.lessons[0].id));
q('#complete-lesson').click();
assert.equal(q('#progress-count').textContent, '0 / 28');

q('#open-search').click();
assert.equal(dialog.open, true);
q('#search-input').value = 'checkpoint';
q('#search-input').dispatchEvent(new Event('input'));
assert.ok(document.querySelectorAll('.search-result').length > 0);
q('#search-input').value = '記憶';
q('#search-input').dispatchEvent(new Event('input'));
assert.ok(document.querySelectorAll('.search-result').length > 0);
q('#search-input').value = 'not-a-real-keyword-99999';
q('#search-input').dispatchEvent(new Event('input'));
assert.ok(q('.search-empty'));
q('#close-search').click();
assert.equal(dialog.open, false);
q('#menu-toggle').click();
assert.equal(q('#menu-toggle').getAttribute('aria-expanded'), 'true');
q('#sidebar-shade').click();
assert.equal(q('#menu-toggle').getAttribute('aria-expanded'), 'false');

let equationCount = 0;
for (const lesson of course.lessons) {
  const {document: doc} = parseHTML(`<html><body>${lesson.html}</body></html>`);
  for (const element of doc.querySelectorAll('.math-source, .math-block')) {
    const source = element.textContent.trim();
    const display = element.classList.contains('math-block');
    const tex = display ? source.slice(2,-2).trim() : source.slice(1,-1);
    const output = katex.renderToString(tex, {displayMode:display, throwOnError:true, trust:false});
    assert.ok(output.includes('class="katex'));
    equationCount++;
  }
}
assert.ok(equationCount >= 15);

export const report = {
  syntax: 'PASS',
  renderedChapters: course.lessons.length,
  interactions: 'PASS: lab, navigation, TOC, progress, notes, English/Chinese search, empty search, mobile menu',
  equations: equationCount,
  limit: 'DOM emulation only; no browser layout or screenshot review',
};
