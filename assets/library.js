/* Local course discovery. Reads existing progress; never writes reader storage. */
(() => {
  'use strict';
  const library = window.LEARNING_LIBRARY;
  if (!library?.courses?.length) return; // Static catalog remains readable without enhancement.
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const defaults = {domain:'all', level:'all', tag:'', q:'', route:''};
  const VIEW_KEY = 'learning-notes:library:card-view:v1';
  const validView = view => view === 'compact' || view === 'detailed';
  const domainNames = new Map(library.domains.map(d => [d.id,d.title]));
  const levelNames = new Map(library.levels.map(l => [l.id,l.title]));
  const routeMap = new Map(library.routes.map(r => [r.id,r]));
  const cards = new Map($$('[data-course]').map(el => [el.dataset.course,el]));
  const classicCourses = [...library.courses].sort((a,b) => a.classicOrder-b.classicOrder);
  const normalize = value => String(value).normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const searchable = new Map(library.courses.map(c => [c.slug,normalize([c.title,c.fullTitle,c.description,c.prerequisite,c.group,domainNames.get(c.domain),...c.tags.map(t => library.tags[t])].join(' '))]));
  let state = {...defaults};

  function readCardView() {
    try {
      const view = window.localStorage.getItem(VIEW_KEY);
      return validView(view) ? view : 'detailed';
    } catch { return 'detailed'; }
  }

  function setCardView(view, remember=false) {
    if (!validView(view)) return;
    document.body.dataset.cardView = view;
    for (const el of $$('[data-view-only]')) el.hidden = el.dataset.viewOnly !== view;
    for (const [slug,card] of cards) card.querySelector('.course-card-link').setAttribute('aria-labelledby',`${view === 'compact' ? 'classic-title' : 'title'}-${slug}`);
    for (const button of $$('[data-card-view-option]')) {
      button.setAttribute('aria-pressed',String(button.dataset.cardViewOption === view));
    }
    $('#card-view-status').textContent = view === 'compact'
      ? '已切換簡易版：原版首頁，單欄課程清單與左圖右文的大圖牌卡。'
      : '已切換詳細版：依領域分類，提供學習路線、搜尋與 tag 篩選。';
    render();
    refreshProgress();
    if (remember) {
      try { window.localStorage.setItem(VIEW_KEY,view); }
      catch { /* Unavailable storage only prevents remembering the display preference. */ }
    }
  }

  function readURL() {
    let params;
    try { params = new URL(window.location.href).searchParams; } catch { return {...defaults}; }
    return {
      domain:domainNames.has(params.get('domain')) ? params.get('domain') : 'all',
      level:levelNames.has(params.get('level')) ? params.get('level') : 'all',
      tag:Object.hasOwn(library.tags,params.get('tag')) ? params.get('tag') : '',
      q:(params.get('q') || '').slice(0,200),
      route:routeMap.has(params.get('route')) ? params.get('route') : ''
    };
  }

  function writeURL(mode) {
    try {
      const url = new URL(window.location.href);
      for (const key of Object.keys(defaults)) {
        url.searchParams.delete(key);
        if (state[key] !== defaults[key]) url.searchParams.set(key,state[key]);
      }
      window.history[mode === 'replace' ? 'replaceState' : 'pushState'](null,'',url.href);
    } catch { /* Filters still work in restricted file viewers. */ }
  }

  function matches(course, filters=state) {
    if (filters.domain !== 'all' && course.domain !== filters.domain) return false;
    if (filters.level !== 'all' && course.level !== filters.level) return false;
    if (filters.tag && !course.tags.includes(filters.tag)) return false;
    if (filters.route && !routeMap.get(filters.route).courses.includes(course.slug)) return false;
    return normalize(filters.q).split(' ').filter(Boolean).every(word => searchable.get(course.slug).includes(word));
  }

  function render() {
    const classic = document.body.dataset.cardView === 'compact';
    const visible = classic ? classicCourses : library.courses.filter(c => matches(c));
    const ids = new Set(visible.map(c => c.slug));
    for (const [slug,card] of cards) card.hidden = !ids.has(slug);
    // Normal browsing stays grouped. A selected route uses its explicit reading order.
    const route = classic ? undefined : routeMap.get(state.route);
    const routeGrid = $('#route-results');
    const classicGrid = $('#classic-results');
    classicGrid.hidden = !classic;
    if (classic) for (const course of classicCourses) classicGrid.append(cards.get(course.slug));
    if (route) {
      for (const slug of route.courses) routeGrid.append(cards.get(slug));
      routeGrid.hidden = false;
    } else {
      routeGrid.hidden = true;
    }
    for (const section of $$('[data-domain-group]')) {
      let count = 0;
      for (const group of [...section.querySelectorAll('[data-course-group]')]) {
        const grid = group.querySelector('.course-grid');
        const groupCourses = library.courses.filter(c => c.domain === section.dataset.domainGroup && c.group === group.querySelector('.subgroup-title').textContent);
        if (!classic && !route) for (const course of groupCourses) grid.append(cards.get(course.slug));
        const n = groupCourses.filter(c => ids.has(c.slug)).length;
        count += n;
        group.hidden = classic || !n || !!route;
      }
      section.hidden = classic || !count || !!route;
      section.querySelector('.domain-result-count').textContent = `${count} 門課程`;
    }
    $('#empty-results').hidden = classic || visible.length !== 0;
    $('#result-count').textContent = `顯示 ${visible.length} / ${library.courses.length} 門課程${state.tag ? ' · #'+library.tags[state.tag] : ''}${route ? ' · '+route.title : ''}`;
    $('#sort-description').textContent = route ? '依建議路線順序' : '領域 → 主題 → 學習起點';
    $('#course-search').value = state.q;
    for (const option of [...$('#domain-filter').options]) option.selected = option.value === state.domain;
    for (const button of $$('[data-level]')) button.setAttribute('aria-pressed',String(button.dataset.level === state.level));
    for (const button of $$('[data-tag]')) button.setAttribute('aria-pressed',String(button.dataset.tag === state.tag));
    for (const button of $$('[data-route]')) button.setAttribute('aria-pressed',String(button.dataset.route === state.route));
    for (const link of $$('[data-domain]')) {
      if (link.dataset.domain === state.domain) link.setAttribute('aria-current','true');
      else link.removeAttribute('aria-current');
    }
    const candidates = library.courses.filter(c => matches(c,{...state,tag:''}));
    for (const counter of $$('[data-tag-count]')) counter.textContent = String(candidates.filter(c => c.tags.includes(counter.dataset.tagCount)).length);
    const labels = {domain:domainNames.get(state.domain),level:levelNames.get(state.level),tag:state.tag && '#'+library.tags[state.tag],q:state.q && `搜尋：${state.q}`,route:route?.title};
    $('#active-filters').innerHTML = Object.entries(labels).filter(([,label]) => label).map(([key,label]) => `<button class="active-chip" type="button" data-remove="${key}" aria-label="移除條件：${esc(label)}">${esc(label)} <span aria-hidden="true">×</span></button>`).join('');
    $('#clear-filters').hidden = !Object.values(labels).some(Boolean);
  }

  function change(patch,{mode='push',scroll=false}={}) {
    state = {...state,...patch};
    render();
    writeURL(mode);
    if (scroll) {
      $('#course-library').scrollIntoView?.({block:'start'});
      $('#catalog-title').focus?.({preventScroll:true});
    }
  }

  function refreshProgress() {
    const ongoing = [];
    for (const course of library.courses) {
      const el = cards.get(course.slug).querySelector('.course-progress');
      el.hidden = true;
      let saved;
      try { saved = JSON.parse(window.localStorage.getItem(`learning-notes:${course.slug}:v1`) || 'null'); } catch { continue; }
      if (!saved || typeof saved !== 'object' || Array.isArray(saved)) continue;
      const completed = new Set(Array.isArray(saved.completed) ? saved.completed.filter(id => course.units.includes(id)) : []);
      const last = course.units.includes(saved.last) ? saved.last : '';
      const label = completed.size === course.units.length ? '已完成' : completed.size || last ? '學習中' : '尚未開始';
      el.hidden = false;
      el.querySelector('[data-progress-label]').textContent = `${label} · ${completed.size} / ${course.units.length} 單元`;
      el.querySelector('progress').value = completed.size;
      if ((completed.size || last) && completed.size < course.units.length) {
        ongoing.push({course,completed:completed.size,id:last || course.units.find(id => !completed.has(id)),hasLast:!!last});
      }
    }
    $('#continue-courses').innerHTML = ongoing.slice(0,3).map(({course,completed,id,hasLast}) => `<a class="continue-card" href="${course.href}#${esc(id)}"><span class="continue-label">${hasLast ? '回到上次閱讀' : '接續未完成單元'} <span aria-hidden="true">↗</span></span><h3>${esc(course.title)}</h3><span>${completed} / ${course.units.length} 單元已完成</span><progress value="${completed}" max="${course.units.length}" aria-label="${esc(course.title)}完成進度"></progress></a>`).join('');
    $('#continue-learning').hidden = document.body.dataset.cardView === 'compact' || !ongoing.length;
  }

  // Build controls before showing them; without JS every static course link works.
  for (const domain of library.domains) {
    const option = document.createElement('option');
    option.value = domain.id;
    option.textContent = domain.title;
    $('#domain-filter').append(option);
  }
  const routeGrid = document.createElement('div');
  routeGrid.id = 'route-results';
  routeGrid.className = 'course-grid';
  routeGrid.hidden = true;
  $('#course-results').prepend(routeGrid);
  $('#catalog-title').setAttribute('tabindex','-1');
  state = readURL();
  document.addEventListener('click', event => {
    const target = event.target.closest?.('[data-domain],[data-level],[data-tag],[data-route],[data-remove],#clear-filters,#empty-reset');
    if (!target) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button > 0) return;
    if (target.hasAttribute('data-domain')) {
      event.preventDefault();
      change({domain:target.dataset.domain,route:''},{scroll:true});
    } else if (target.hasAttribute('data-level')) {
      change({level:target.dataset.level});
    } else if (target.hasAttribute('data-tag')) {
      const insideCard = !!target.closest('[data-course]');
      change({tag:state.tag === target.dataset.tag ? '' : target.dataset.tag},{scroll:insideCard});
    } else if (target.hasAttribute('data-route')) {
      const r = routeMap.get(target.dataset.route);
      // Routes may span domains (e.g. statistics → health), so start with all domains.
      change({...defaults,route:state.route === r.id ? '' : r.id},{scroll:true});
    } else if (target.hasAttribute('data-remove')) {
      const key = target.dataset.remove;
      change({[key]:defaults[key]});
      ($('#clear-filters').hidden ? $('#course-search') : $('#clear-filters')).focus?.({preventScroll:true});
    } else {
      change({...defaults});
      $('#course-search').focus?.({preventScroll:true});
    }
  });
  $('#course-search').addEventListener('input', event => change({q:event.target.value.slice(0,200)},{mode:'replace'}));
  $('#course-search').maxLength = 200;
  $('#domain-filter').addEventListener('change', event => change({domain:event.target.value,route:''}));
  for (const button of $$('[data-card-view-option]')) {
    button.addEventListener('click', () => {
      if (button.dataset.cardViewOption !== document.body.dataset.cardView) setCardView(button.dataset.cardViewOption,true);
    });
  }
  window.addEventListener('popstate', () => {state = readURL();render();});
  window.addEventListener('pageshow',refreshProgress);
  window.addEventListener('focus',refreshProgress);
  window.addEventListener('storage',event => {
    if (!event.key || event.key === VIEW_KEY) setCardView(validView(event.newValue) ? event.newValue : 'detailed');
    if (!event.key || event.key !== VIEW_KEY && event.key.startsWith('learning-notes:')) refreshProgress();
  });
  for (const el of $$('.enhancement')) el.hidden = false;
  setCardView(readCardView());
})();
