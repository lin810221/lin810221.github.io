/* Local explanatory labs. These never contact provider APIs. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const instructions = '請以繁體中文回答，依據資料說明。';
  const schema = {type:'object',properties:{answer:{type:'string'},sources:{type:'array',items:{type:'string'}}},required:['answer','sources'],additionalProperties:false};
  const providers = {
    openai:{name:'OpenAI',endpoint:'POST /v1/responses',note:'Responses API：reasoning 與 text.format 的支援依模型而異。'},
    gemini:{name:'Gemini',endpoint:'POST /v1beta/interactions',note:'Interactions API：generation_config 控制生成；新模型的採樣參數可能被忽略。'},
    claude:{name:'Claude',endpoint:'POST /v1/messages',note:'Messages API：effort 放在 output_config；thinking 模式的支援依模型而異。'},
  };
  function requestFor(provider, maxTokens, effort, structured) {
    let body;
    if(provider === 'openai') {
      body = {model:'YOUR_OPENAI_MODEL',instructions,input:'什麼是 AI Agent？',max_output_tokens:maxTokens,store:false};
      if(effort !== 'default') body.reasoning = {effort};
      if(structured) body.text = {format:{type:'json_schema',name:'answer',schema,strict:true}};
    } else if(provider === 'gemini') {
      body = {model:'YOUR_GEMINI_MODEL',system_instruction:instructions,input:'什麼是 AI Agent？',generation_config:{max_output_tokens:maxTokens},store:false};
      if(effort !== 'default') body.generation_config.thinking_level = effort;
      if(structured) body.response_format = {type:'text',mime_type:'application/json',schema};
    } else {
      body = {model:'YOUR_CLAUDE_MODEL',max_tokens:maxTokens,system:instructions,messages:[{role:'user',content:'什麼是 AI Agent？'}]};
      if(effort !== 'default') { body.thinking = {type:'adaptive'}; body.output_config = {effort}; }
      if(structured) { body.output_config ||= {}; body.output_config.format = {type:'json_schema',schema}; }
    }
    return body;
  }
  window.LLM_LABS = {requestFor};
  window.renderCourseOverview = ({course,saved,escapeHTML,main,toc,footer}) => {
    const last = saved.last || course.lessons[0].id;
    const minutes = course.lessons.reduce((sum,lesson) => sum + lesson.minutes,0);
    main.innerHTML = `<section class="course-hero" id="intro"><div class="eyebrow">LLM SERVICES & AI AGENTS <span>／ 從理解到建構</span></div><h1>LLM APIs<span class="hero-period">.</span></h1><h2 class="hero-subtitle">從一次對話，<br>走向能行動的 AI。</h2><p class="hero-description">理解 OpenAI、Gemini、Claude 的功能與參數，掌握工具呼叫、資料檢索與記憶，親手把模型組成可控制的 Agent。</p><div class="hero-meta"><span><b>38</b> 個完整章節</span><span><b>3</b> 大供應商</span><span><b>12</b> 份 Python 範例</span><span>約 <b>${Math.round(minutes / 60 * 10) / 10}</b> 小時純閱讀</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last ? '繼續學習' : '從第一章開始'} <span aria-hidden="true">→</span></a><a class="text-link" href="#overview/roadmap">瀏覽學習路線 <span aria-hidden="true">↓</span></a></div></section><div class="provider-strip"><a class="provider-item" href="#09-openai-responses"><strong><span class="status-dot"></span>OpenAI</strong><small>RESPONSES API</small></a><a class="provider-item" href="#11-gemini-interactions"><strong><span class="status-dot"></span>Gemini</strong><small>INTERACTIONS API</small></a><a class="provider-item" href="#13-claude-messages"><strong><span class="status-dot"></span>Claude</strong><small>MESSAGES API</small></a></div>
    <section id="parameter-lab"><div class="section-header"><h2>相同目的，三種 API 表達</h2><span>EXPLORE THE REQUEST</span></div><div class="api-lab"><div class="lab-tabs" role="tablist" aria-label="API 供應商">${Object.entries(providers).map(([key,p],index) => `<button id="tab-${key}" class="provider-tab" role="tab" data-provider="${key}" aria-controls="request-panel" aria-selected="${index === 0}" tabindex="${index === 0 ? 0 : -1}">${p.name}</button>`).join('')}</div><div class="lab-form"><label for="lab-max-tokens"><span>最大輸出預算 <output id="lab-max-value" class="mono">2048</output></span><input id="lab-max-tokens" type="range" min="512" max="8192" step="512" value="2048"></label><label for="lab-effort"><span>推理深度（需模型支援）</span><select id="lab-effort"><option value="default">使用模型預設</option value="low">low</option><option value="medium">medium</option><option value="high">high</option></select></label><label class="lab-check"><input id="lab-structured" type="checkbox"><span>要求符合 JSON Schema 的結構化答案</span></label><p class="lab-field-note" id="lab-provider-note"></p></div><div id="request-panel" role="tabpanel" aria-labelledby="tab-openai"><div class="api-request-header"><span id="lab-endpoint"></span><button class="copy-button" id="copy-request">⧉ 複製 JSON</button></div><pre class="api-request" id="lab-request" aria-live="polite"></pre></div><div class="lab-caption">本機教學示意，不會呼叫 API。模型名稱是待替換值；參數、Schema 子集與組合限制仍須以你選用的模型文件核對。最大輸出預算不等於可見答案長度。</div></div></section>
    <section id="sampling-lab"><div class="section-header"><h2>讓抽象的採樣，變得看得見</h2><span>A CONCEPTUAL DISTRIBUTION</span></div><div class="sampling-panel"><div class="sampling-controls"><label for="sample-temperature"><span>Temperature <output id="sample-temperature-value">1.0</output></span><input id="sample-temperature" type="range" min="0.1" max="2" step="0.1" value="1"></label><label for="sample-top-p"><span>Top-p <output id="sample-top-p-value">1.0</output></span><input id="sample-top-p" type="range" min="0.1" max="1" step="0.05" value="1"></label></div><div class="probability-chart" id="probability-chart" aria-live="polite"></div><p class="sampling-note">這四個候選與 logits 是人造數據，用來理解 softmax 和 nucleus sampling，不代表任何真實模型。調整這裡不會更動上方請求；部分新模型已不開放這些採樣設定。</p></div></section>
    <section id="roadmap"><div class="section-header"><h2>你的學習路線</h2><span>FROM API TO AGENT</span></div><div class="module-list">${course.groups.map(group => { const lessons = course.lessons.filter(lesson => lesson.group === group.id); return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${group.number}</span><div><div class="module-name">${escapeHTML(group.title)}</div><div class="module-description">${escapeHTML(group.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS <span aria-hidden="true">↗</span></span></a>`; }).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>所有 Python 範例預設離線執行。三家 API 範例只有加上 <code>--live</code> 才送出真實請求，且需要你自己的 Key 與可用模型。<br>官方文件核對日期：2026-10-29。模型、價格、參數與服務可用性會變動，各章保留原始官方來源。</div><div class="course-bridge"><span aria-hidden="true">⌘</span><div>已經讀過 LangGraph？<br>這門課補上模型服務、工具協定與 Agent 的基礎，再到 <a href="../langgraph/index.html">LangGraph 課程 ↗</a> 練習更複雜的工作流程。</div></div>${footer}`;
    toc.innerHTML = '<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於這份教學</a><a href="#overview/parameter-lab">三家 API 實驗室</a><a href="#overview/sampling-lab">採樣概念實驗室</a><a href="#overview/roadmap">學習路線</a><a href="#overview/before-start">開始之前</a></div><div class="toc-tip"><p>先理解共通概念，<br>再核對供應商細節。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋教學</p><p><a href="examples/README.md">Python 範例說明 ↗</a></p><p>此課程的閱讀進度<br>與 LangGraph 分開儲存。</p></div>';
    initRequestLab(); initSamplingLab();
  };
  window.renderCourseOverview.courseSlug = 'llm';
  function initRequestLab() {
    let selected = 'openai';
    function draw() {
      const maxTokens = Number($('#lab-max-tokens').value);
      $('#lab-max-value').textContent = String(maxTokens);
      $('#lab-endpoint').textContent = providers[selected].endpoint;
      $('#lab-provider-note').textContent = providers[selected].note;
      $('#request-panel').setAttribute('aria-labelledby','tab-' + selected);
      $('#lab-request').textContent = JSON.stringify(requestFor(selected,maxTokens,$('#lab-effort').value || 'default',$('#lab-structured').checked),null,2);
      document.querySelectorAll('.provider-tab').forEach(tab => { const active = tab.dataset.provider === selected; tab.setAttribute('aria-selected',String(active)); tab.tabIndex = active ? 0 : -1; });
    }
    document.querySelectorAll('.provider-tab').forEach(tab => {
      tab.addEventListener('click',() => { selected = tab.dataset.provider; draw(); });
      tab.addEventListener('keydown',event => { const keys = Object.keys(providers); let index = keys.indexOf(selected); if(event.key === 'ArrowRight') index = (index + 1) % keys.length; else if(event.key === 'ArrowLeft') index = (index + keys.length - 1) % keys.length; else if(event.key === 'Home') index = 0; else if(event.key === 'End') index = keys.length - 1; else return; event.preventDefault(); selected = keys[index]; draw(); $('#tab-' + selected).focus(); });
    });
    ['#lab-max-tokens','#lab-effort','#lab-structured'].forEach(selector => $(selector).addEventListener('input',draw));
    $('#lab-effort').addEventListener('change',draw);
    $('#lab-structured').addEventListener('change',draw);
    $('#copy-request').addEventListener('click',async event => {
      const button = event.currentTarget;
      try {
        const text = $('#lab-request').textContent;
        if(navigator.clipboard?.writeText && window.isSecureContext) await navigator.clipboard.writeText(text);
        else { const field = document.createElement('textarea'); field.value = text; field.style.position = 'fixed'; field.style.opacity = '0'; document.body.append(field); field.select(); const ok = document.execCommand('copy'); field.remove(); if(!ok) throw new Error('Clipboard unavailable'); }
        button.textContent = '✓ 已複製';
      } catch { button.textContent = '請選取 JSON 後複製'; }
    });
    draw();
  }
  function initSamplingLab() {
    const names = ['建議','可以','或許','但是'];
    const logits = [2.8,1.9,0.9,0.3];
    function draw() {
      const temperature = Number($('#sample-temperature').value);
      const topP = Number($('#sample-top-p').value);
      $('#sample-temperature-value').textContent = temperature.toFixed(1);
      $('#sample-top-p-value').textContent = topP.toFixed(2);
      const weights = logits.map(logit => Math.exp((logit - logits[0]) / temperature));
      const sum = weights.reduce((a,b) => a+b,0);
      const probabilities = weights.map(weight => weight / sum);
      let cumulative = 0;
      const kept = probabilities.map(probability => { const keep = cumulative < topP; cumulative += probability; return keep ? probability : 0; });
      const total = kept.reduce((a,b) => a+b,0);
      $('#probability-chart').innerHTML = kept.map((value,index) => { const probability = value / total; return `<div class="probability-row"><span>${names[index]}</span><div class="probability-track"><div class="probability-fill" style="width:${probability * 100}%"></div></div><output>${(probability * 100).toFixed(1)}%</output></div>`; }).join('');
    }
    $('#sample-temperature').addEventListener('input',draw);
    $('#sample-top-p').addEventListener('input',draw);
    draw();
  }
})();
