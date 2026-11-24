/* Actual KaTeX DOM fallback and static pre-render idempotence, without browser layout. */
import assert from 'node:assert/strict';
import {parseHTML} from '../.qa/vendor/linkedom.mjs';
import katex from '../assets/vendor/katex/katex.mjs';
import {renderHTMLMath} from './render_math.mjs';

const fixture='<span class="math-source" data-tex="x_i&lt;y_j" data-display="false">$x_i&lt;y_j$</span><!--math-end-->';
const rendered=renderHTMLMath(fixture,'fixture');
assert.ok(rendered.includes('class="katex"'));
assert.equal(renderHTMLMath(rendered,'idempotence'),rendered);
assert.throws(()=>renderHTMLMath('<div data-tex="\\badcommand" data-display="true">$$x$$</div><!--math-end-->','invalid'),/invalid/);
const {window,document}=parseHTML('<html><body><main>'+rendered+fixture+'<p class="lesson-summary"><span class="math-source" data-tex="\\frac{1}{n}" data-display="false">$1/n$</span></p></main></body></html>');
Object.assign(globalThis,{window,document});
window.katex=katex;
await import('../assets/math.js');
const root=document.querySelector('main');
window.LearningNotesMath.render(root);
assert.equal(root.querySelectorAll('.katex').length,3);
assert.equal(root.querySelectorAll('[data-math-error]').length,0);
const before=root.innerHTML;window.LearningNotesMath.render(root);assert.equal(root.innerHTML,before);
const bad=document.createElement('span');bad.className='math-source';bad.dataset.tex='\\badcommand';root.append(bad);
window.LearningNotesMath.render(root);assert.equal(bad.dataset.mathError,'true');assert.ok(bad.textContent.includes('公式'));
const pending=document.createElement('span');pending.className='math-source';pending.dataset.tex='a+b';root.append(pending);delete window.katex;
window.LearningNotesMath.render(root);assert.equal(pending.dataset.mathPending,'true');window.katex=katex;
window.LearningNotesMath.render(root);assert.ok(pending.querySelector('.katex'));assert.equal(pending.dataset.mathPending,undefined);
// Numbering suite expects a course-shaped window; this test has no reader routes.
export const report={mathRuntime:'PASS',prerenderIdempotence:'PASS',formulaFallback:'PASS: inline, summary, error visibility, deferred library'};
