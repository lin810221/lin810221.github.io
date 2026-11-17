/* Shared visual supplement; existing lessons, labs, IDs and storage remain independent. */
(() => {
  'use strict';
  const original=window.renderCourseOverview,course=window.COURSE;
  if(typeof original!=='function'||original.courseSlug!==course?.slug||!course.visuals?.length)return;
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function render(props){
    original(props);
    const {main,toc}=props;
    const section=document.createElement('section');section.id='health-visuals';section.className='health-visual-index';
    section.innerHTML=`<div class="section-header"><h2>圖解索引：看見關係，再回課文</h2><span>${course.visuals.length} ILLUSTRATED EXPLANATIONS</span></div><p>每個閱讀單元都有圖解與對應讀圖任務。先辨識構造、分母或情境，再追圖中的路徑；相同圖在不同單元有不同閱讀重點。原有程式與資料範例可作選讀輔助。</p><label for="health-visual-filter">選擇章節</label><select id="health-visual-filter"><option value="all" selected>全部圖解</option>${course.groups.map(g=>`<option value="${esc(g.id)}">${esc(g.number)} ${esc(g.title)}</option>`).join('')}</select><p id="health-visual-count" class="health-visual-count" aria-live="polite"></p><div id="health-visual-grid" class="health-visual-grid"></div><div class="health-visual-actions"><a class="primary-button" href="${esc(course.studyBundle)}" download>下載圖解與讀圖任務 ↓</a><a class="text-link" href="study/README.md">離線閱讀方式 ↗</a><a class="text-link" href="study/read-tasks.md">全部讀圖任務 ↗</a></div><p>圖解補強：${esc(course.visualUpdated)}。原課指南、程式與資料的查核日期依各章來源，這次圖解更新不將它們改稱新版。示意圖省略細節處見圖說；個別圖片再用來源另列。</p>`;
    const footer=main.querySelector('.page-footer');if(footer)footer.before(section);else main.append(section);
    const meta=main.querySelector('.hero-meta');
    if(meta){const codeBadge=[...meta.children].find(n=>n.textContent.includes('Python'));const badge=`<b>${course.visuals.length}</b> 張中文圖解`;if(codeBadge){codeBadge.innerHTML=badge;codeBadge.classList.add('health-visual-tag');}else meta.insertAdjacentHTML('beforeend',`<span class="health-visual-tag">${badge}</span>`);}
    const tocLinks=toc.querySelector('.toc-links');if(tocLinks)tocLinks.insertAdjacentHTML('beforeend','<a href="#overview/health-visuals">圖解索引與學習包</a>');
    const select=section.querySelector('#health-visual-filter'),grid=section.querySelector('#health-visual-grid'),count=section.querySelector('#health-visual-count');
    const draw=()=>{const selected=select.value,figures=selected==='all'?course.visuals:course.visuals.filter(f=>f.group===selected);count.textContent=`顯示 ${figures.length} / ${course.visuals.length} 張；點圖可放大，或進入對應課文。`;grid.innerHTML=figures.map(f=>{const lessons=course.lessons.filter(l=>l.visual===f.id),number=String(course.visuals.indexOf(f)+1).padStart(2,'0');return `<figure class="health-visual-card" data-visual="${esc(f.id)}"><a href="${esc(f.file)}" target="_blank" rel="noopener" aria-label="放大：${esc(f.title)}"><img src="${esc(f.file)}" alt="${esc(f.description)}" width="${f.width||860}" height="${f.height||520}" loading="lazy"></a><figcaption><strong>圖 ${number} · ${esc(f.title)}</strong><small>${esc(f.kind)}${f.reusedFrom?' · 本學習空間原創圖再用':''}</small>${lessons.map(l=>`<a class="text-link" href="#${esc(l.id)}">${esc(l.title)} →</a>`).join('<br>')}</figcaption></figure>`;}).join('');};
    select.addEventListener('change',draw);draw();
  }
  render.courseSlug=course.slug;window.renderCourseOverview=render;
})();
