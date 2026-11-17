/* Shared acceptance for the five visual supplements; runs in each reader worker. */
import assert from 'node:assert/strict';
import {Event,parseHTML} from '../.qa/vendor/linkedom.mjs';
import {readFile} from 'node:fs/promises';

export async function verifyHealthVisuals(){
  const course=window.COURSE,q=s=>document.querySelector(s);
  const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
  const checkOverview=()=>{
    assert.equal(document.querySelectorAll('#health-visuals').length,1);
    assert.equal(document.querySelectorAll('.health-visual-card').length,48);
    assert.ok(q('.hero-meta').textContent.includes('張中文圖解'));
    assert.equal(q('#health-visuals a[download]').getAttribute('href'),course.studyBundle);
    assert.equal(q('.toc-links a[href="#overview/health-visuals"]').textContent,'圖解索引與學習包');
  };
  navigate('overview');checkOverview();
  const saved=localStorage.getItem(`learning-notes:${course.slug}:v1`);
  const select=q('#health-visual-filter'),options=[...select.querySelectorAll('option')];
  function choose(value){
    for(const option of options)option.selected=false;
    options.find(o=>o.value===value).selected=true;
    select.dispatchEvent(new Event('change'));
  }
  for(const group of course.groups){
    choose(group.id);
    const cards=[...document.querySelectorAll('.health-visual-card')];
    assert.equal(cards.length,3);
    assert.ok(q('#health-visual-count').textContent.includes('3 / 48'));
    for(const card of cards){
      const figure=course.visuals.find(f=>f.id===card.dataset.visual);
      assert.equal(figure.group,group.id);
      const image=card.querySelector('img');
      assert.equal(image.getAttribute('src'),figure.file);
      assert.ok(image.getAttribute('alt').length>20);
      assert.equal(image.parentNode.getAttribute('target'),'_blank');
      assert.equal(image.parentNode.getAttribute('rel'),'noopener');
      assert.deepEqual([...card.querySelectorAll('figcaption a')].map(a=>a.getAttribute('href')),course.lessons.filter(l=>l.visual===figure.id).map(l=>'#'+l.id));
    }
  }
  choose('all');checkOverview();
  assert.equal(localStorage.getItem(`learning-notes:${course.slug}:v1`),saved);
  for(const lesson of course.lessons){
    navigate(lesson.id);
    const figure=course.visuals.find(f=>f.id===lesson.visual);
    assert.equal(document.querySelectorAll('.health-figure').length,1);
    assert.equal(q('.health-figure img').getAttribute('src'),figure.file);
    assert.ok(q('.health-read-task').textContent.includes(lesson.visualTask));
    assert.ok(q('.health-figure-sources').textContent.includes('2026-11-16'));
    assert.equal(q('.health-figure-sources a[href="study-pack.zip"]').getAttribute('href'),course.studyBundle);
    assert.ok(q('.toc-links a[href$="/visual-reading"]'));
  }
  navigate('overview');checkOverview();
  const ids=[...document.querySelectorAll('[id]')].map(el=>el.id);
  assert.equal(ids.length,new Set(ids).size);
  const css=await readFile(new URL('../assets/health-visuals.css',import.meta.url),'utf8');
  assert.ok(parseHTML('<style>'+css+'</style>').document.querySelector('style').sheet.cssRules.length>=15);
  const current=JSON.parse(localStorage.getItem(`learning-notes:${course.slug}:v1`)),before=JSON.parse(saved);
  assert.deepEqual(current.completed,before.completed);
  assert.deepEqual(current.notes,before.notes);
  assert.equal(current.last,course.lessons.at(-1).id);
  return '48 zoomable figures; 16 chapter filters; 96 lesson mappings/tasks; remount and stored progress: PASS';
}
