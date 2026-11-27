/* Check the user's reported cases in generated HTML, not only in Markdown. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {parseHTML} from '../.qa/vendor/linkedom.mjs';
const root=new URL('../',import.meta.url);
async function course(slug){return JSON.parse((await readFile(new URL(`${slug}/assets/course-data.js`,root),'utf8')).split('window.COURSE = ')[1].trim().replace(/;$/,''));}
function section(doc,heading){let h=[...doc.querySelectorAll('h2')].find(heading);assert.ok(h);let nodes=[];for(let n=h.nextElementSibling;n&&n.tagName!=='H2';n=n.nextElementSibling)nodes.push(n.outerHTML);return parseHTML('<html><body>'+nodes.join('')+'</body></html>').document;}
function equations(doc){return [...doc.querySelectorAll('.math-block')].map(e=>{assert.equal(e.getAttribute('data-rendered'),'katex');assert.ok(e.querySelector('.katex'));assert.ok(e.querySelector('annotation[encoding="application/x-tex"]'));return e.getAttribute('data-tex');}).join('\n');}

const stats=await course('applied-statistics');
const lesson=stats.lessons.find(l=>l.id==='17-discrete-families');
const doc=parseHTML('<html><body>'+lesson.html+'</body></html>').document;
for(const id of ['4-4-1','4-4-2','4-4-3','4-4-4-poisson']){
  const part=section(doc,h=>h.id===id),tex=equations(part);
  assert.ok(tex.includes('P(X='),id+': own PMF');assert.ok(tex.includes('E[X]'),id+': own mean');assert.ok(tex.includes('\\operatorname{Var}(X)'),id+': own variance');
  assert.equal(part.querySelectorAll('[data-math-error]').length,0);
}
assert.ok(equations(section(doc,h=>h.id==='4-4-1')).includes('\\begin{cases}'));
assert.ok(!section(doc,h=>h.id==='4-4-1').body.textContent.includes('各機率1/k'));
const torch=await course('pytorch');
const lossDoc=parseHTML('<html><body>'+torch.lessons.find(l=>l.id==='18-losses').html+'</body></html>').document;
assert.ok(equations(section(lossDoc,h=>h.textContent.includes('BCEWithLogitsLoss'))).includes('sigma'));
assert.ok(equations(section(lossDoc,h=>h.textContent.includes('MSELoss'))).includes('sum'));
const econ=await course('economics');
assert.ok(econ.lessons.find(l=>l.id==='23-perfect-competition').summaryHTML.includes('class="katex"'));
const transform=await course('transformer');
const grad=transform.lessons.find(l=>l.id==='005-gradients').html;
assert.ok(grad.includes('L\\left(w-\\varepsilon \\right)'), 'finite difference retains both perturbations');
for(const [slug,id,word] of [['rag','03-pipeline','corpus_version'],['pytorch','04-tensors','dtype=torch.float32'],['image-recognition','024-classification-exercises','Conv2d']]){
  const c=await course(slug);const d=parseHTML('<html><body>'+c.lessons.find(l=>l.id===id).html+'</body></html>').document;
  assert.ok([...d.querySelectorAll('code')].some(n=>n.textContent.includes(word)),slug+': API/code remains code');
}
export const report={distributions:'4 PMFs and 4 sets of moments in their own sections PASS',otherSubjects:'BCE, MSE, economic summary and finite differences PASS',codeIdentity:'APIs remain copyable code PASS',limit:'DOM inspection, not a real-browser screenshot'};
