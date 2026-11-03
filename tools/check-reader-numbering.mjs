/* Check user-visible numbering at real chapter boundaries for every reader. */
import assert from 'node:assert/strict';
import {Event} from '../.qa/vendor/linkedom.mjs';

export function verifyReaderNumbering(){
  const {window,document,location,localStorage}=globalThis,course=window.COURSE,q=s=>document.querySelector(s);
  const savedHash=location.hash,storageKey=`learning-notes:${course.slug}:v1`,saved=JSON.parse(localStorage.getItem(storageKey)||'{}');
  const positions=new Map(),groups=[...document.querySelectorAll('.nav-group')];
  assert.equal(groups.length,course.groups.length);
  let checked=0,boundaries=0;
  course.groups.forEach((group,chapterIndex)=>{
    const units=course.lessons.filter(l=>l.group===group.id),links=[...groups[chapterIndex].querySelectorAll('.chapter-link')];
    assert.equal(links.length,units.length);
    units.forEach((unit,i)=>{
      const number=String(i+1).padStart(2,'0'),chapter=/^\d+$/.test(group.number)?`第 ${Number(group.number)} 章`:group.number==='附'?'附錄':group.title;
      positions.set(unit.id,{number,label:`${chapter} · 單元 ${number}`,group,count:units.length});
      assert.equal(links[i].querySelector('.chapter-number').textContent,number,`${course.slug}/${unit.id}: numbering must restart within its chapter`);
      assert.equal(links[i].querySelector('.chapter-label').textContent,unit.title);assert.equal(links[i].getAttribute('href'),'#'+unit.id);checked++;
    });
  });
  const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
  for(const group of course.groups){
    const units=course.lessons.filter(l=>l.group===group.id);
    for(const unit of [...new Set([units[0],units.at(-1)])]){
      navigate(unit.id);const pos=positions.get(unit.id),index=course.lessons.indexOf(unit),kicker=q('.lesson-kicker').textContent;
      const expectedChapter=/^\d+$/.test(group.number)?`CHAPTER ${group.number}`:`APPENDIX${group.number==='附'?'':' '+group.number}`;
      assert.ok(kicker.includes(expectedChapter));assert.ok(kicker.includes(`UNIT ${pos.number} OF ${pos.count}`));assert.ok(q('.lesson-breadcrumb').textContent.endsWith('單元 '+pos.number));
      assert.equal(q('.lesson-header h1').textContent,unit.title);
      if(index){const prev=course.lessons[index-1];assert.equal(q('.pagination-link.previous').getAttribute('href'),'#'+prev.id);assert.ok(q('.pagination-link.previous small').textContent.includes(positions.get(prev.id).label));}
      if(index+1<course.lessons.length){const next=course.lessons[index+1];assert.equal(q('.pagination-link.next').getAttribute('href'),'#'+next.id);assert.ok(q('.pagination-link.next small').textContent.includes(positions.get(next.id).label));}
      boundaries++;
    }
  }
  // Search results must locate their chapter, since local unit numbers repeat.
  const target=course.lessons.find(l=>l.group===course.groups[1].id),oldQuery=q('#search-input').value;
  q('#open-search').click();q('#search-input').value=target.title;q('#search-input').dispatchEvent(new Event('input'));
  const result=q(`.search-result[href="#${target.id}"]`);assert.ok(result);assert.equal(result.querySelector('.mono').textContent,positions.get(target.id).label);
  q('#search-input').value=oldQuery;q('#close-search').click();
  const after=JSON.parse(localStorage.getItem(storageKey)||'{}');assert.deepEqual(after.completed,saved.completed);assert.deepEqual(after.notes,saved.notes);
  navigate(savedHash.slice(1)||'overview');
  return {units:checked,chapterBoundaries:boundaries,search:'chapter + local unit',savedNotesAndProgress:'preserved'};
}
