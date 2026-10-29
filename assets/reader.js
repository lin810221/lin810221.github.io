/* Local, buildless course reader. No API keys, analytics or network requests. */
(() => {
  'use strict';
  const course = window.COURSE;
  const $ = selector => document.querySelector(selector);
  const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const STORAGE_KEY = `learning-notes:${course?.slug || 'langgraph'}:v1`;
  let storageOK = true;
  let saved = {completed: [], notes: {}, last: ''};
  try {
    const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    if (raw && typeof raw === 'object') {
      saved.completed = Array.isArray(raw.completed) ? raw.completed.filter(id => course.lessons.some(l => l.id === id)) : [];
      saved.notes = raw.notes && typeof raw.notes === 'object' && !Array.isArray(raw.notes) ? raw.notes : {};
      saved.last = course.lessons.some(l => l.id === raw.last) ? raw.last : '';
    }
  } catch { storageOK = false; }
  const save = () => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(saved)); storageOK = true; }
    catch { storageOK = false; }
    return storageOK;
  };
  let currentId = null;
  let observer;
  let toastTimeout;
  function toast(message) {
    clearTimeout(toastTimeout);
    $('#toast').textContent = message;
    $('#toast').classList.add('visible');
    toastTimeout = setTimeout(() => $('#toast').classList.remove('visible'), 2600);
  }
  function updateProgress() {
    const count = new Set(saved.completed).size;
    $('#course-progress').max = course.lessons.length;
    $('#course-progress').value = count;
    $('#progress-count').textContent = `${count} / ${course.lessons.length}`;
    document.querySelectorAll('.chapter-link').forEach(link => {
      const completed = saved.completed.includes(link.dataset.lesson);
      link.querySelector('.chapter-check').textContent = completed ? '✓' : '';
      if (completed) link.querySelector('.chapter-check').setAttribute('aria-label', '已完成');
      else link.querySelector('.chapter-check').removeAttribute('aria-label');
    });
  }
  function buildNavigation() {
    $('#chapter-nav').innerHTML = course.groups.map(group => `<section class="nav-group"><h2 class="nav-group-title"><span class="mono">${group.number}</span>${escapeHTML(group.title)}</h2>${course.lessons.filter(l => l.group === group.id).map(lesson => `<a class="chapter-link" data-lesson="${lesson.id}" href="#${lesson.id}"><span class="chapter-number">${lesson.id.slice(0, 2)}</span><span class="chapter-label">${escapeHTML(lesson.title)}</span><span class="chapter-check"></span></a>`).join('')}</section>`).join('');
    updateProgress();
  }
  const footer = `<footer class="page-footer"><span>Learning Notes <span>／ 一次理解一個概念。</span></span><span class="mono">UPDATED ${escapeHTML((course.updated || '2026-10-29').replaceAll('-', '.'))} · ${escapeHTML(course.footerLabel || 'PYTHON')}</span></footer>`;
  function overview() {
    if (course.slug && typeof window.renderCourseOverview === 'function' && window.renderCourseOverview.courseSlug === course.slug) {
      window.renderCourseOverview({course, saved, escapeHTML, main:$('#main'), toc:$('#page-toc'), footer});
      return;
    }
    const last = saved.last || course.lessons[0].id;
    const totalMinutes = course.lessons.reduce((sum, l) => sum + l.minutes, 0);
    $('#main').innerHTML = `<section class="course-hero" id="intro"><div class="eyebrow">THE COMPLETE GUIDE <span>／ 從零到實務</span></div><h1>LangGraph<span class="hero-period">.</span></h1><h2 class="hero-subtitle">讓 AI 的每一步，<br>都在你的掌握之中。</h2><p class="hero-description">從第一個節點開始，親手建立有狀態、有記憶、能等待人類決策的工作流程。一步步理解原理，寫出可以驗證的程式。</p><div class="hero-meta"><span><b>28</b> 個完整章節</span><span><b>12</b> 份可執行範例</span><span>約 <b>${Math.round(totalMinutes / 60 * 10) / 10}</b> 小時純閱讀</span><span>不含動手練習時間</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last ? '繼續學習' : '從第一章開始'} <span aria-hidden="true">→</span></a><a class="text-link" href="#overview/roadmap">瀏覽學習路線 <span aria-hidden="true">↓</span></a></div></section>
    <section id="try-it"><div class="section-header"><h2>先看看，一張圖如何思考</h2><span>AN INTERACTIVE WALKTHROUGH</span></div><div class="graph-lab"><div class="lab-header"><span><span class="status-dot"></span> 知識助理的工作流程</span><span class="lab-badge">6 STEPS · STATEFUL</span></div><div class="lab-body"><div class="graph-track" role="list" aria-label="示意流程的六個節點">${[['START','接收問題'],['ROUTE','分類'],['RETRIEVE','找資料'],['DRAFT','寫草稿'],['INTERRUPT','人工審核'],['END','完成']].map((item, i) => `${i ? '<span class="graph-connector" aria-hidden="true"></span>' : ''}<div role="listitem" class="graph-node" data-step="${i}"><small>${item[0]}</small><span>${item[1]}</span></div>`).join('')}</div><div class="lab-state" aria-live="polite"><div class="lab-state-info"><strong id="lab-step-title"></strong><span id="lab-step-description"></span></div><pre id="lab-state-code"></pre></div><div class="lab-controls"><span id="lab-counter"></span><div><button id="lab-reset" class="secondary-button" aria-label="重設流程示範">↺ 重設</button><button id="lab-next" class="secondary-button"></button></div></div></div><div class="lab-caption">這是瀏覽器中的概念示範，使用固定資料，不會呼叫模型。完整 Python 實作在第 25 章。</div></div></section>
    <section id="roadmap"><div class="section-header"><h2>你的學習路線</h2><span>BUILD UNDERSTANDING, STEP BY STEP</span></div><div class="module-list">${course.groups.map(group => {
      const lessons = course.lessons.filter(l => l.group === group.id);
      return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${group.number}</span><div><div class="module-name">${escapeHTML(group.title)}</div><div class="module-description">${escapeHTML(group.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS <span aria-hidden="true">↗</span></span></a>`;
    }).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>基礎章節只需要 Python；需要 API Key 的模型範例會明確註明。建議邊閱讀、邊修改程式，將「看得懂」變成「做得到」。<br>範例驗證基準：LangGraph ${course.baseline}。新版功能另作說明，每章附官方來源。</div>${footer}`;
    $('#page-toc').innerHTML = `<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於這份教學</a><a href="#overview/try-it">互動流程示範</a><a href="#overview/roadmap">學習路線</a><a href="#overview/before-start">開始之前</a></div><div class="toc-tip"><p>學習，不需要一次完成。</p><p>每章都可以留下自己的筆記，完成後勾選，讓理解一步步累積。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋教學</p><p><a href="examples/README.md">Python 範例說明 ↗</a></p></div>`;
    initLab();
  }
  function initLab() {
    let step = 0;
    const states = [
      {title:'01 ／ 收到問題',description:'輸入先放進 State。後續的節點讀取同一份資料契約，再回傳需要更新的欄位。',state:{question:'LangGraph 的記憶怎麼運作？'}},
      {title:'02 ／ 決定下一步',description:'路由檢查問題類型。這裡需要文件依據，因此選擇檢索分支。',state:{question:'LangGraph 的記憶怎麼運作？',route:'retrieve'}},
      {title:'03 ／ 尋找依據',description:'檢索節點加入文件。它只回傳 docs 的更新，不需要重新傳回整份 State。',state:{route:'retrieve',docs:['[D1] Checkpointer：對話狀態','[D2] Store：跨對話資料']}},
      {title:'04 ／ 產生草稿',description:'草稿引用取得的資料。這個示範以固定文字模擬，實務上可在此接入 LLM。',state:{draft:'Checkpointer 保存 thread 狀態；Store 保存跨 thread 資料。[D1][D2]',approved:null}},
      {title:'05 ／ 等待人工審核',description:'interrupt 暫停執行。只有收到外部決策，才會繼續；單純重新整理頁面不等於核准。',state:{status:'waiting_for_review',approved:null}},
      {title:'06 ／ 完成',description:'核准後才建立最終答案。這一輪結束，checkpoint 可以保存後續對話需要的狀態。',state:{approved:true,status:'done',answer:'Checkpointer 保存 thread 狀態；Store 保存跨 thread 資料。[D1][D2]'}}
    ];
    function draw() {
      document.querySelectorAll('.graph-node').forEach((node, i) => { node.classList.toggle('current', i === step); node.classList.toggle('done', i < step); if (i === step) node.setAttribute('aria-current','step'); else node.removeAttribute('aria-current'); });
      $('#lab-step-title').textContent = states[step].title;
      $('#lab-step-description').textContent = states[step].description;
      $('#lab-state-code').textContent = JSON.stringify(states[step].state, null, 2);
      $('#lab-counter').textContent = `STEP ${String(step + 1).padStart(2,'0')} / 06`;
      $('#lab-next').textContent = step === 4 ? '核准並繼續 →' : step === 5 ? '流程已完成 ✓' : '執行下一步 →';
      $('#lab-next').disabled = step === 5;
      $('#lab-reset').disabled = step === 0;
    }
    $('#lab-next').addEventListener('click', () => { if (step < 5) step++; draw(); });
    $('#lab-reset').addEventListener('click', () => { step = 0; draw(); });
    draw();
  }
  function renderLesson(lesson) {
    const index = course.lessons.indexOf(lesson);
    const group = course.groups.find(g => g.id === lesson.group);
    const completed = saved.completed.includes(lesson.id);
    $('#main').innerHTML = `<header class="lesson-header"><div class="lesson-breadcrumb"><a href="#overview">${escapeHTML(course.shortTitle || 'LangGraph')}</a><span>/</span>${escapeHTML(group.title)}<span>/</span>第 ${index + 1} 章</div><div class="lesson-kicker">CHAPTER ${lesson.id.slice(0, 2)} <span>／ ${course.lessons.length}</span></div><h1>${escapeHTML(lesson.title)}</h1><p class="lesson-summary">${escapeHTML(lesson.summary)}</p><div class="lesson-meta"><span>約 ${lesson.minutes} 分鐘閱讀</span>${lesson.tags.map(tag => `<span class="tag">${escapeHTML(tag)}</span>`).join('')}<span>${completed ? '✓ 已完成' : '按自己的步調閱讀'}</span></div></header><article class="lesson-content">${lesson.html}</article>${lesson.example ? `<div class="example-download"><div><strong>本章可執行範例</strong><span class="mono">examples/${escapeHTML(lesson.example)}</span></div><a class="secondary-button" href="examples/${escapeHTML(lesson.example)}" download>下載 Python 範例 ↓</a></div>` : ''}<section class="notes-box"><div class="notes-heading"><label for="lesson-notes">寫下你的理解</label><span id="note-status">${storageOK ? '自動儲存於此瀏覽器' : '目前無法儲存，離開頁面前請自行備份'}</span></div><textarea id="lesson-notes" placeholder="有什麼想法、疑問，或值得記住的細節？"></textarea></section><div class="completion-row"><button class="complete-button" id="complete-lesson" aria-pressed="${completed}">${completed ? '✓ 已完成本章' : '○ 標記本章已完成'}</button><p>理解需要練習，進度不需要趕。</p></div><nav class="lesson-pagination" aria-label="章節切換">${index > 0 ? `<a class="pagination-link previous" href="#${course.lessons[index - 1].id}"><small>← 上一章</small><strong>${escapeHTML(course.lessons[index - 1].title)}</strong></a>` : '<a class="pagination-link previous" href="#overview"><small>← 回到課程</small><strong>課程總覽</strong></a>'}${index < course.lessons.length - 1 ? `<a class="pagination-link next" href="#${course.lessons[index + 1].id}"><small>下一章 →</small><strong>${escapeHTML(course.lessons[index + 1].title)}</strong></a>` : '<a class="pagination-link next" href="#overview"><small>回顧你的學習 →</small><strong>回到學習路線</strong></a>'}</nav>${footer}`;
    if (lesson.example && course.exampleBundle) {
      const download = $('.example-download a');
      download.setAttribute('href',course.exampleBundle);
      download.textContent = '下載完整範例包 ↓';
    }
    const notes = $('#lesson-notes');
    notes.value = typeof saved.notes[lesson.id] === 'string' ? saved.notes[lesson.id] : '';
    notes.addEventListener('input', () => {
      saved.notes[lesson.id] = notes.value;
      $('#note-status').textContent = save() ? '已儲存於此瀏覽器' : '儲存空間不可用，請複製筆記備份';
    });
    $('#complete-lesson').addEventListener('click', event => {
      const nowComplete = !saved.completed.includes(lesson.id);
      saved.completed = saved.completed.filter(id => id !== lesson.id);
      if (nowComplete) saved.completed.push(lesson.id);
      const persisted = save();
      event.currentTarget.setAttribute('aria-pressed', String(nowComplete));
      event.currentTarget.textContent = nowComplete ? '✓ 已完成本章' : '○ 標記本章已完成';
      updateProgress();
      toast(persisted ? (nowComplete ? '已記錄這一步的累積。' : '已更新閱讀進度。') : '目前無法儲存進度，重新開啟後可能遺失。');
    });
    document.querySelectorAll('.lesson-content table').forEach(table => { const wrapper = document.createElement('div'); wrapper.className = 'table-scroll'; wrapper.tabIndex = 0; wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label','表格，可橫向捲動'); table.before(wrapper); wrapper.append(table); });
    document.querySelectorAll('.lesson-content .codehilite, .lesson-content > pre').forEach(block => {
      const pre = block.tagName === 'PRE' ? block : block.querySelector('pre');
      if (!pre) return;
      const shell = document.createElement('div');
      shell.className = 'code-shell';
      const language = block.dataset.language || (pre.querySelector('code')?.className.replace('language-', '') || 'CODE');
      shell.innerHTML = `<div class="code-header"><span>${escapeHTML(language.toUpperCase())}</span><button class="copy-button" aria-label="複製程式碼">⧉ 複製</button></div>`;
      block.before(shell);
      shell.append(block);
      shell.querySelector('button').addEventListener('click', async event => {
        const button = event.currentTarget;
        try { await copy(pre.textContent); button.textContent = '✓ 已複製'; setTimeout(() => { if (button.isConnected) button.textContent = '⧉ 複製'; }, 1600); }
        catch { toast('無法自動複製，請選取程式碼後按 Ctrl+C。'); }
      });
    });
    document.querySelectorAll('.lesson-content a[href^="https://"]').forEach(link => { link.target = '_blank'; link.rel = 'noopener noreferrer'; });
    if (typeof window.renderMathInElement === 'function') {
      window.renderMathInElement($('.lesson-content'), {delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},{left:'\\(',right:'\\)',display:false},{left:'\\[',right:'\\]',display:true}],throwOnError:false,trust:false,ignoredTags:['script','noscript','style','textarea','pre','code']});
    }
    const headings = [...document.querySelectorAll('.lesson-content h2, .lesson-content h3')];
    $('#page-toc').innerHTML = `<h2 class="toc-label">本章內容</h2><div class="toc-links">${headings.map(h => `<a class="${h.tagName === 'H3' ? 'subheading' : ''}" href="#${lesson.id}/${h.id}">${escapeHTML(h.textContent)}</a>`).join('')}</div><div class="toc-tip"><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋內容</p><p><kbd>Alt</kbd> + <kbd>←</kbd> / <kbd>→</kbd><br>切換上一章、下一章</p><p>公式以 LaTeX 語法撰寫，<br>可以離線顯示。</p></div>`;
    observeHeadings(headings);
  }
  async function copy(text) {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      try { await navigator.clipboard.writeText(text); return; } catch { /* fallback for local files */ }
    }
    const field = document.createElement('textarea');
    field.value = text; field.style.position = 'fixed'; field.style.opacity = '0';
    document.body.append(field); field.select();
    const ok = document.execCommand('copy'); field.remove();
    if (!ok) throw new Error('Clipboard unavailable');
  }
  function observeHeadings(headings) {
    if (observer) observer.disconnect();
    if (!window.IntersectionObserver) return;
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        document.querySelectorAll('.toc-links a').forEach(a => a.classList.toggle('current', a.getAttribute('href').endsWith('/' + entry.target.id)));
      });
    }, {rootMargin:'-90px 0px -65% 0px'});
    headings.forEach(h => observer.observe(h));
  }
  function closeSidebar() { $('#sidebar').classList.remove('open'); $('#sidebar-shade').hidden = true; $('#menu-toggle').setAttribute('aria-expanded','false'); }
  function render() {
    const [requested = 'overview', encodedAnchor] = location.hash.slice(1).split('/');
    const lesson = course.lessons.find(l => l.id === requested);
    const id = lesson ? lesson.id : 'overview';
    if (id !== currentId) {
      if (observer) observer.disconnect();
      currentId = id;
      if (lesson) { renderLesson(lesson); saved.last = id; save(); }
      else overview();
      document.title = `${lesson ? lesson.title : (course.title || 'LangGraph 完整教學')} · Learning Notes`;
      document.querySelectorAll('.chapter-link').forEach(link => { const active = link.dataset.lesson === id; link.classList.toggle('active', active); if(active) link.setAttribute('aria-current','page'); else link.removeAttribute('aria-current'); });
      $('.overview-link').classList.toggle('active', !lesson);
      if (!lesson) $('.overview-link').setAttribute('aria-current','page'); else $('.overview-link').removeAttribute('aria-current');
      window.scrollTo(0,0);
      $('#main').focus({preventScroll:true});
    }
    closeSidebar();
    if (encodedAnchor) {
      let anchor;
      try { anchor = decodeURIComponent(encodedAnchor); } catch { anchor = encodedAnchor; }
      requestAnimationFrame(() => document.getElementById(anchor)?.scrollIntoView({behavior:'auto',block:'start'}));
    }
  }
  function showSearch() { if (!$('#search-dialog').open) $('#search-dialog').showModal(); $('#search-input').focus(); search($('#search-input').value); }
  function search(query) {
    const q = query.trim().toLocaleLowerCase();
    if (!q) { $('#search-results').innerHTML = `<div class="search-empty">從一個問題開始。<br>${escapeHTML(course.searchHint || '試試 State、interrupt、記憶 或 Send。')}</div>`; return; }
    const terms = q.split(/\s+/).filter(Boolean);
    const results = course.lessons.map(lesson => {
      const title = lesson.title.toLocaleLowerCase();
      const full = `${lesson.title} ${lesson.summary} ${lesson.tags.join(' ')} ${lesson.text}`.toLocaleLowerCase();
      return {lesson, score:terms.every(t => full.includes(t)) ? terms.reduce((score,t) => score + (title.includes(t) ? 8 : lesson.summary.toLocaleLowerCase().includes(t) ? 3 : 1),0) : 0};
    }).filter(r => r.score > 0).sort((a,b) => b.score - a.score);
    function mark(text) {
      const escaped = escapeHTML(text);
      const safeTerms = terms.map(escapeHTML).map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      return escaped.replace(new RegExp(`(${safeTerms.join('|')})`,'gi'),'<mark>$1</mark>');
    }
    $('#search-results').innerHTML = results.length ? results.map(({lesson}) => {
      const pos = lesson.text.toLocaleLowerCase().indexOf(terms[0]);
      const snippet = pos >= 0 ? lesson.text.slice(Math.max(0,pos-30),pos+110).replace(/[#`*\n]/g,' ') : lesson.summary;
      return `<a class="search-result" href="#${lesson.id}"><strong><span class="mono">${lesson.id.slice(0,2)}</span> · ${mark(lesson.title)}</strong><small>${mark(snippet)}</small></a>`;
    }).join('') : '<div class="search-empty">找不到符合的章節。<br>可以換成較短的詞，或試試 API 的英文名稱。</div>';
  }
  if (!course?.lessons?.length) { $('#main').textContent = '教材資料尚未載入，請確認 assets/course-data.js 存在。'; return; }
  buildNavigation(); render();
  window.addEventListener('hashchange',render);
  $('#open-search').addEventListener('click',showSearch);
  $('#close-search').addEventListener('click',() => $('#search-dialog').close());
  $('#search-input').addEventListener('input',event => search(event.target.value));
  $('#search-input').addEventListener('keydown',event => { if(event.key === 'Enter') { const first = $('.search-result'); if(first) { $('#search-dialog').close(); location.hash = first.getAttribute('href'); } } });
  $('#search-results').addEventListener('click',event => { if(event.target.closest('a')) $('#search-dialog').close(); });
  $('#search-dialog').addEventListener('click',event => { if(event.target === event.currentTarget) { const rect = event.currentTarget.getBoundingClientRect(); if(event.clientY < rect.top || event.clientY > rect.bottom || event.clientX < rect.left || event.clientX > rect.right) event.currentTarget.close(); } });
  $('#print-page').addEventListener('click',() => window.print());
  $('#menu-toggle').addEventListener('click',() => { const open = $('#sidebar').classList.toggle('open'); $('#sidebar-shade').hidden = !open; $('#menu-toggle').setAttribute('aria-expanded', String(open)); });
  $('#sidebar-shade').addEventListener('click',closeSidebar);
  document.addEventListener('keydown',event => {
    if((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); showSearch(); }
    if(event.key === 'Escape') closeSidebar();
    if(event.target.matches('input, textarea, [contenteditable]') || $('#search-dialog').open) return;
    if(event.altKey && ['ArrowLeft','ArrowRight'].includes(event.key)) {
      const index = course.lessons.findIndex(l => l.id === currentId);
      const target = course.lessons[index + (event.key === 'ArrowRight' ? 1 : -1)];
      if(target) { event.preventDefault(); location.hash = target.id; }
    }
  });
})();
