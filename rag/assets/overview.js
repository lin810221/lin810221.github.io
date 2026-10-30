/* Offline teaching labs. Fictional public data; no model calls or API keys. */
(() => {
  'use strict';
  const normalize = value => String(value).normalize('NFC').replace(/\r\n?/g, '\n').trim();
  const documents = [
    {id:'leave',title:'休假辦法',text:'特休申請必須提前三個工作日提出，並由直屬主管核准。病假請於當日上午通知主管。',page:2,version:'2026-10',tenant:'demo',roles:['reader'],active:true},
    {id:'travel',title:'差旅規範',text:'國內出差住宿費上限為每晚新臺幣 2400 元，請保留住宿收據。差旅報銷應在返程後十個工作日內提交。國際出差住宿額度依核准計畫。',page:5,version:'2026-10',tenant:'demo',roles:['reader'],active:true},
    {id:'remote',title:'遠端工作',text:'遠端工作每週最多兩日，須在前一週由主管核准。遠端工作期間仍須遵守資料保護規範。',page:8,version:'2026-10',tenant:'demo',roles:['reader'],active:true},
    {id:'it',title:'帳號與 VPN',text:'忘記密碼請使用員工入口的密碼重設功能。VPN 錯誤碼 VPN-403 表示授權檢查失敗，請確認帳號權限。',page:12,version:'2026-10',tenant:'demo',roles:['reader'],active:true},
    {id:'travel-old',title:'舊差旅規範',text:'國內出差住宿費上限為每晚新臺幣 1800 元。',page:5,version:'2024-01',tenant:'demo',roles:['reader'],active:false},
    {id:'salary',title:'薪資設定（虛構）',text:'薪資設定的管理權限僅供人資使用。虛構主管薪資為每月 999999 元。',page:1,version:'2026-10',tenant:'demo',roles:['hr'],active:true},
    {id:'other',title:'另一租戶休假',text:'特休申請必須提前三十個工作日提出。',page:1,version:'2026-10',tenant:'other',roles:['reader'],active:true}
  ];
  function tokenize(value) {
    const terms = [];
    for (const match of normalize(value).toLowerCase().matchAll(/[a-z0-9]+(?:[-_][a-z0-9]+)*|[\u3400-\u9fff]+/g)) {
      const term = match[0];
      if (/^[\u3400-\u9fff]+$/.test(term)) {
        const chars = Array.from(term);
        terms.push(...chars);
        for (let i=0;i<chars.length-1;i++) terms.push(chars[i]+chars[i+1]);
      } else terms.push(term);
    }
    return terms;
  }
  function bm25(query, docs, k=5) {
    if(k<=0 || !docs.length) return [];
    const counts = docs.map(doc => {const map=new Map();for(const t of tokenize(doc.text)) map.set(t,(map.get(t)||0)+1);return map;});
    const lengths = counts.map(map => [...map.values()].reduce((a,b)=>a+b,0));
    const average = lengths.reduce((a,b)=>a+b,0)/docs.length;
    if(!average) return [];
    const df = new Map();
    for(const count of counts) for(const term of count.keys()) df.set(term,(df.get(term)||0)+1);
    const terms = new Set(tokenize(query));
    return docs.map((doc,i)=>({doc,score:[...terms].reduce((total,t)=> {
      const f=counts[i].get(t)||0;
      if(!f) return total;
      const idf=Math.log(1+(docs.length-df.get(t)+.5)/(df.get(t)+.5));
      return total+idf*f*2.2/(f+1.2*(.25+.75*lengths[i]/average));
    },0)})).filter(row=>row.score>0).sort((a,b)=>b.score-a.score || a.doc.id.localeCompare(b.doc.id)).slice(0,k);
  }
  function rrf(rankings,c=60) {
    if(!(c>0) || !Number.isFinite(c)) throw new RangeError('c must be positive');
    const totals=new Map();
    for(const ranking of rankings) {
      const seen=new Set();
      ranking.forEach((row,i)=> {if(seen.has(row.doc.id)) return;seen.add(row.doc.id);const previous=totals.get(row.doc.id);totals.set(row.doc.id,{doc:row.doc,score:(previous?.score||0)+1/(c+i+1)});});
    }
    return [...totals.values()].sort((a,b)=>b.score-a.score || a.doc.id.localeCompare(b.doc.id));
  }
  function split(text,size,overlap) {
    if(!Number.isInteger(size) || !Number.isInteger(overlap) || size<=0 || overlap<0 || overlap>=size) throw new RangeError('Invalid chunk size or overlap');
    const chars=Array.from(normalize(text)),chunks=[];
    for(let start=0;start<chars.length;) {
      const end=Math.min(start+size,chars.length);
      chunks.push({start,end,text:chars.slice(start,end).join('')});
      if(end===chars.length) break;
      start=end-overlap;
    }
    return chunks;
  }
  function metrics(ranking,relevant,k=3) {
    if(!Number.isInteger(k) || k<=0 || Object.values(relevant).some(x=>x<0)) throw new RangeError('Invalid metric parameters');
    const seen=new Set();
    const gains=ranking.slice(0,k).map(id=> {const g=seen.has(id)?0:(relevant[id]||0);seen.add(id);return g;});
    const hits=gains.filter(g=>g>0).length,total=Object.values(relevant).filter(g=>g>0).length;
    const dcg=gains.reduce((s,g,i)=>s+(2**g-1)/Math.log2(i+2),0);
    const ideal=Object.values(relevant).sort((a,b)=>b-a).slice(0,k).reduce((s,g,i)=>s+(2**g-1)/Math.log2(i+2),0);
    const first=gains.findIndex(g=>g>0);
    return {precision:hits/k,recall:total?hits/total:0,mrr:first<0?0:1/(first+1),ndcg:ideal?dcg/ideal:0};
  }
  window.RAGLab={tokenize,bm25,rrf,split,metrics};

  function overview({course,saved,escapeHTML:e,main,toc,footer}) {
    const last=saved.last||course.lessons[0].id;
    const minutes=course.lessons.reduce((sum,l)=>sum+l.minutes,0);
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">RETRIEVAL AUGMENTED GENERATION <span>／ 從文件到可靠答案</span></div><h1>RAG<span class="hero-period">.</span></h1><h2 class="hero-subtitle">先找到依據，<br>再寫出答案。</h2><p class="hero-description">讓知識不只被儲存，也能被正確找到。從第一份文件、第一次檢索，到有引用、可評估、能持續更新的知識助理。</p><div class="hero-meta"><span><b>42</b> 個完整章節</span><span><b>16</b> 份 Python 範例</span><span><b>3</b> 個互動實驗室</span><span>約 <b>${Math.round(minutes/6)/10}</b> 小時純閱讀</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last?'繼續學習':'從第一章開始'} <span aria-hidden="true">→</span></a><a class="text-link" href="#overview/retrieval-lab">先玩一次檢索 <span aria-hidden="true">↓</span></a></div><div class="rag-principles"><span><b>01</b> 找得到</span><span><b>02</b> 有依據</span><span><b>03</b> 可查證</span></div></section>
    <section id="retrieval-lab"><div class="section-header"><h2>問題，如何找到依據？</h2><span>LAB 01 · RETRIEVE & CITE</span></div><p class="rag-section-intro">輸入問題，看看候選、分數與原句回答。試試同義擴展，也觀察角色和租戶如何改變可用資料。</p><div class="rag-lab"><form id="rag-search-form"><label class="rag-label" for="rag-query">想問什麼？</label><div class="rag-query-row"><input id="rag-query" value="特休申請提前" maxlength="120" autocomplete="off" placeholder="例如：出差住飯店的額度"><button class="primary-button" type="submit">尋找依據 →</button></div><div class="rag-presets"><button type="button" data-query="國內出差住宿費上限">差旅額度</button><button type="button" data-query="出差住飯店的額度">口語問法</button><button type="button" data-query="薪資設定">權限範圍</button><button type="button" data-query="火星基地氧氣費率">資料不足</button></div><div class="rag-controls"><label>檢索方式<select id="rag-mode"><option value="bm25" selected>BM25 原始查詢</option><option value="expanded">同義擴展 + RRF</option></select></label><label>示範角色<select id="rag-role"><option value="reader" selected>一般讀者</option><option value="hr">讀者＋人資</option></select></label><label>示範租戶<select id="rag-tenant"><option value="demo" selected>星河工作室</option><option value="other">另一租戶</option></select></label><label>候選上限 <output id="rag-k-value">3</output><input id="rag-k" type="range" min="1" max="4" value="3"></label></div></form><div class="rag-results" aria-live="polite"><div class="rag-result-heading"><span id="rag-scope"></span><span class="mono" id="rag-score-label"></span></div><p id="rag-variants" class="rag-small"></p><div id="rag-hits"></div><div class="rag-answer"><span class="eyebrow">EVIDENCE → ANSWER</span><p id="rag-answer-text"></p><small id="rag-answer-status"></small></div></div><p class="rag-caption">這裡實際執行字詞檢索、排名融合與原句擷取，不呼叫模型。所有資料公開且虛構；角色切換是教學示範，正式授權應由伺服器執行。</p></div></section>
    <section id="chunk-lab"><div class="section-header"><h2>一份文件，要切成多大？</h2><span>LAB 02 · CHUNK & OVERLAP</span></div><p class="rag-section-intro">改寫內容或拖動滑桿，觀察片段邊界。計數單位為 Unicode 字元，與模型 token 不同。</p><div class="rag-lab rag-chunk-lab"><label class="rag-label" for="chunk-text">文件內容</label><textarea id="chunk-text" rows="4" maxlength="600">國內出差住宿費上限為每晚新臺幣 2400 元，請保留住宿收據。差旅報銷應在返程後十個工作日內提交。國際出差的住宿額度依核准計畫，不能沿用國內上限。特休申請須提前三個工作日，並由直屬主管核准。</textarea><div class="rag-sliders"><label for="chunk-size">每塊大小 <output id="chunk-size-value">40</output><input id="chunk-size" type="range" min="20" max="120" step="5" value="40"></label><label for="chunk-overlap">重疊字元 <output id="chunk-overlap-value">10</output><input id="chunk-overlap" type="range" min="0" max="39" value="10"></label></div><div id="chunk-summary" class="rag-chunk-summary" aria-live="polite"></div><div id="chunk-results" class="rag-chunks"></div><p class="rag-caption">offset 對應標準化文字，起點包含、終點不包含。重疊保留邊界資訊，也增加重複與索引成本。最多顯示前 60 段。</p></div></section>
    <section id="metrics-lab"><div class="section-header"><h2>找到幾份，排在哪裡？</h2><span>LAB 03 · MEASURE RETRIEVAL</span></div><p class="rag-section-intro">已知 A 是直接證據（2 分），B 是部分相關（1 分），X 不相關。改變前三名，看看四種指標各在意什麼。</p><div class="rag-lab rag-metrics-lab"><div class="rag-rank-controls">${[1,2,3].map((rank,i)=>`<label for="metric-rank-${rank}">第 ${rank} 名<select id="metric-rank-${rank}"><option value="A" ${i===1?'selected':''}>A · 直接證據</option><option value="B" ${i===2?'selected':''}>B · 部分相關</option><option value="X" ${i===0?'selected':''}>X · 不相關</option></select></label>`).join('')}</div><div id="metric-results" class="rag-metric-results" aria-live="polite"></div><p id="metric-explanation" class="rag-small"></p><p class="rag-caption">k = 3，固定以文件為單位。重複 ID 只在第一次計分，但仍占排名；nDCG 使用 gain = 2^rel − 1。完整定義與手算在第 30 章。</p></div></section>
    <section id="roadmap"><div class="section-header"><h2>從理解，到自己做出來</h2><span>YOUR LEARNING PATH</span></div><div class="module-list">${course.groups.map(group=> {const lessons=course.lessons.filter(l=>l.group===group.id);return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${group.number}</span><div><div class="module-name">${e(group.title)}</div><div class="module-description">${e(group.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS <span aria-hidden="true">↗</span></span></a>`;}).join('')}</div></section><div id="before-start" class="reading-note"><strong>開始之前</strong><br>會讀 Python 即可開始，數學公式逐步說明。16 份範例預設可離線執行；真正 Embedding 與 LLM 呼叫須明確加入 <code>--live</code>。所有規章與數字都是虛構教材。<br>純閱讀時間不含動手練習。進度與筆記保存在此瀏覽器，無法自動跨裝置同步。</div><div class="rag-bridge"><span aria-hidden="true">↗</span><p>先了解模型服務，可讀 <a href="../llm/index.html">LLM 與 AI Agents</a>；想管理有狀態的檢索迴圈，可接著讀 <a href="../langgraph/index.html">LangGraph</a>。<br><a href="examples.zip" download>下載完整 Python 範例包 ↓</a></p></div>${footer}`;
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於這份教學</a><a href="#overview/retrieval-lab">檢索與引用實驗室</a><a href="#overview/chunk-lab">切塊與重疊實驗室</a><a href="#overview/metrics-lab">評估指標實驗室</a><a href="#overview/roadmap">學習路線</a><a href="#overview/before-start">開始之前</a></div><div class="toc-tip"><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋全部章節</p><p><a href="examples/README.md">範例執行說明 ↗</a></p><p>從問題出發，<br>讓每個答案都有來處。</p></div>`;
    const $=selector=>main.querySelector(selector);
    function search() {
      const query=$('#rag-query').value.trim(),mode=$('#rag-mode').value,tenant=$('#rag-tenant').value;
      const roles=$('#rag-role').value==='hr'?['reader','hr']:['reader'];
      const allowed=documents.filter(d=>d.tenant===tenant&&d.active&&d.roles.some(r=>roles.includes(r)));
      const k=Number($('#rag-k').value);
      $('#rag-k-value').textContent=k;
      const replacements=[['住飯店','住宿費 上限'],['連不上','VPN 故障'],['休假','特休 申請']];
      const variants=[query];
      if(mode==='expanded') for(const [from,to] of replacements) if(query.includes(from)) variants.push(query.replaceAll(from,to));
      const unique=[...new Set(variants)];
      const hits=mode==='expanded'?rrf(unique.map(q=>bm25(q,allowed,allowed.length))).slice(0,k):bm25(query,allowed,k);
      $('#rag-scope').textContent=`可用 ${allowed.length} 份文件 → 找到 ${hits.length} 份候選`;
      $('#rag-score-label').textContent=mode==='expanded'?'RRF SCORE':'BM25 SCORE';
      $('#rag-variants').textContent=`查詢：${unique.join(' ／ ') || '請先輸入問題'}`;
      $('#rag-hits').innerHTML=hits.length?hits.map((row,i)=>`<article class="rag-hit"><div class="rag-hit-head"><span class="rag-source-id">S${i+1}</span><strong>${e(row.doc.title)}</strong><span class="mono">${row.score.toFixed(mode==='expanded'?5:3)}</span></div><p>${e(row.doc.text)}</p><small>${e(row.doc.id)} · v${e(row.doc.version)} · p${row.doc.page}</small></article>`).join(''):'<p class="rag-empty">目前的可見資料沒有命中。可改寫問題、確認範圍，或保留資料不足的結果。</p>';
      const terms=new Set(unique.flatMap(tokenize));
      const sentences=hits.flatMap((row,i)=>row.doc.text.split(/(?<=[。！？.!?])\s*/).filter(Boolean).map(text=>({text,label:`S${i+1}`,score:terms.size?[...new Set(tokenize(text))].filter(t=>terms.has(t)).length/terms.size:0})));
      sentences.sort((a,b)=>b.score-a.score);
      const best=sentences[0];
      const sufficient=best&&best.score>=.35;
      $('#rag-answer-text').textContent=sufficient?`${best.text} [${best.label}]`:'資料不足，請補充或改寫問題。';
      $('#rag-answer-status').textContent=sufficient?'原句擷取示範 · 詞元覆蓋啟發式，不代表完整語意判定':'INSUFFICIENT EVIDENCE · 本示範沒有產生模型答案';
    }
    $('#rag-search-form').addEventListener('submit',event=>{event.preventDefault();search();});
    for(const id of ['#rag-mode','#rag-role','#rag-tenant']) $(id).addEventListener('change',search);
    $('#rag-k').addEventListener('input',search);
    main.querySelectorAll('[data-query]').forEach(button=>button.addEventListener('click',()=>{$('#rag-query').value=button.dataset.query;search();}));
    function drawChunks() {
      const size=Number($('#chunk-size').value);
      $('#chunk-overlap').max=String(size-1);
      const overlap=Math.min(Number($('#chunk-overlap').value),size-1);
      $('#chunk-overlap').value=String(overlap);
      const text=normalize($('#chunk-text').value),chunks=split(text,size,overlap),length=Array.from(text).length;
      $('#chunk-size-value').textContent=size;
      $('#chunk-overlap-value').textContent=overlap;
      const indexed=chunks.reduce((sum,c)=>sum+c.end-c.start,0);
      $('#chunk-summary').textContent=`${length} 字元 ／ 步長 ${size-overlap} ／ ${chunks.length} 段 ／ 索引文字 ${indexed} 字元${chunks.length>60?'（顯示前 60 段）':''}`;
      $('#chunk-results').innerHTML=chunks.length?chunks.slice(0,60).map((c,i)=>`<div class="rag-chunk"><div><b>CHUNK ${String(i+1).padStart(2,'0')}</b><span>[${c.start}:${c.end}]</span></div><p>${e(c.text)}</p></div>`).join(''):'<p class="rag-empty">空文件不產生片段。</p>';
    }
    for(const id of ['#chunk-size','#chunk-overlap','#chunk-text']) $(id).addEventListener('input',drawChunks);
    function drawMetrics() {
      const ranking=[1,2,3].map(i=>$(`#metric-rank-${i}`).value);
      const values=metrics(ranking,{A:2,B:1},3);
      const labels=[['precision','Precision@3'],['recall','Recall@3'],['mrr','MRR@3'],['ndcg','nDCG@3']];
      $('#metric-results').innerHTML=labels.map(([key,label])=>`<div><span>${label}</span><output data-metric="${key}">${values[key].toFixed(3)}</output></div>`).join('');
      $('#metric-explanation').textContent=`目前排名 ${ranking.join(' → ')}。Precision 看相關比例，Recall 看兩份相關文件找齊多少，MRR 看第一個相關位置，nDCG 同時看等級與位置。${new Set(ranking).size<ranking.length?'有重複文件：不重複給分，仍占用名次。':''}`;
    }
    for(const i of [1,2,3]) $(`#metric-rank-${i}`).addEventListener('change',drawMetrics);
    search();drawChunks();drawMetrics();
  }
  overview.courseSlug='rag';
  window.renderCourseOverview=overview;
})();
