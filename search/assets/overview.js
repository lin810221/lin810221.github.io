/* Deterministic browser teaching labs. No engine, model or network calls. */
(() => {
  'use strict';
  const tokens=text=>String(text).normalize('NFKC').toLocaleLowerCase('en').match(/[\p{L}\p{N}_]+/gu)||[];
  function analyze(text,mode='words'){
    if(mode==='words')return tokens(text);
    if(mode!=='bigrams')throw new RangeError('未知斷詞模式');
    return tokens(text).flatMap(token=>/^\p{Script=Han}+$/u.test(token)&&[...token].length>1?Array.from({length:[...token].length-1},(_,i)=>[...token].slice(i,i+2).join('')):[token]);
  }
  const lexicalDocs=[{id:'A',text:'usb hub'},{id:'B',text:'usb hub hub hub hub manual manual manual manual manual'},{id:'C',text:'usb cable'}];
  function bm25(query,k1,b){
    if(!Number.isFinite(k1)||k1<=0||!Number.isFinite(b)||b<0||b>1)throw new RangeError('k1 > 0，b 介於 0 與 1');
    const docs=lexicalDocs.map(d=>({...d,terms:tokens(d.text)})),avg=docs.reduce((s,d)=>s+d.terms.length,0)/docs.length;
    return docs.map(d=>({id:d.id,text:d.text,score:[...new Set(tokens(query))].reduce((score,t)=>{
      const tf=d.terms.filter(x=>x===t).length,df=docs.filter(x=>x.terms.includes(t)).length;
      return score+(tf?Math.log(1+(docs.length-df+.5)/(df+.5))*tf*(k1+1)/(tf+k1*(1-b+b*d.terms.length/avg)):0);
    },0)})).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
  }
  function filtered(budget,k=3){
    if(!Number.isInteger(budget)||budget<1||budget>8)throw new RangeError('候選預算為 1–8');
    const ranked=['B1','B2','A1','B3','A2','B4','A3','A4'],allowed=id=>id.startsWith('A');
    return {scanned:ranked.slice(0,budget),post:ranked.slice(0,budget).filter(allowed).slice(0,k),eligibleFirst:ranked.filter(allowed).slice(0,k)};
  }
  function rrf(lists,c=60,weights=lists.map(()=>1)){
    if(!Number.isFinite(c)||c<0||weights.length!==lists.length||weights.some(w=>!Number.isFinite(w)||w<0)||!weights.some(w=>w>0))throw new RangeError('RRF 常數與權重不合法');
    const scores=new Map();lists.forEach((list,j)=>{if(new Set(list).size!==list.length)throw new RangeError('單路 ID 不可重複');if(!weights[j])return;list.forEach((id,i)=>scores.set(id,(scores.get(id)||0)+weights[j]/(c+i+1)));});
    return [...scores].map(([id,score])=>({id,score})).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
  }
  function lifecycle(){
    let source={revision:1,active:true},index={revision:1,active:true},checkpoint=1,events=[{revision:1,active:true}];
    return {snapshot:()=>({source:{...source},index:index?{...index}:null,checkpoint,events:events.length,visible:Boolean(index&&source.active&&index.active&&source.revision===index.revision)}),
      action(kind){
        if(kind==='update'||kind==='delete'){source={revision:source.revision+1,active:kind==='update'};events.push({...source});return '來源提交，索引尚未同步；查詢重新檢查來源。';}
        if(kind==='old'){return '拒絕舊 revision=1：以來源最新狀態為準，不讓舊事件復活文件。';}
        if(kind==='replay'){for(let i=checkpoint;i<events.length;i++){const event=events[i];if(event.revision===source.revision)index=source.active?{...source}:null;checkpoint=i+1;}return '單一有序 worker 已同步並保存水位。';}
        throw new RangeError('未知事件');}
    };
  }
  function capacity(n,d,bits,m,copies,headroom,retain){
    if(![n,d,bits,m,copies].every(Number.isInteger)||n<1||d<1||m<0||copies<1||![8,16,32].includes(bits)||!Number.isFinite(headroom)||headroom<1||n>1e9||d>1e5)throw new RangeError('容量參數超出範圍或不是有效整數');
    const vectors=n*d*bits/8,originals=retain&&bits!==32?n*d*4:0,graph=n*m*2*4,total=(vectors+originals+graph)*copies*headroom;
    return {vectors,originals,graph,total,GB:total/1e9,GiB:total/2**30};
  }
  function quality(exact,ann,grades,latencies,k=3){
    if(!Array.isArray(exact)||!Array.isArray(ann)||new Set(exact).size!==exact.length||new Set(ann).size!==ann.length||grades.some(g=>!Number.isFinite(g)||g<0)||!latencies.length||latencies.some(t=>!Number.isFinite(t)||t<0))throw new RangeError('ID 需唯一，等級與延遲需為非負數');
    const truth=exact.slice(0,k),found=ann.slice(0,k),recall=truth.length?found.filter(x=>truth.includes(x)).length/truth.length:null;
    const gain=list=>list.slice(0,k).reduce((sum,g,i)=>sum+(2**g-1)/Math.log2(i+2),0),ideal=gain([...grades].sort((a,b)=>b-a));
    const sorted=[...latencies].sort((a,b)=>a-b),quantile=p=>{const index=(sorted.length-1)*p,lo=Math.floor(index),hi=Math.ceil(index);return sorted[lo]+(sorted[hi]-sorted[lo])*(index-lo);};
    return {recall,ndcg:ideal?gain(grades)/ideal:null,p50:quantile(.5),p95:quantile(.95)};
  }
  window.SearchLab=Object.freeze({analyze,bm25,filtered,rrf,lifecycle,capacity,quality});
  const lab=(n,title,body)=>`<section class="search-lab" id="search-lab-${n}"><header><span class="mono">LAB ${String(n).padStart(2,'0')}</span><h3>${title}</h3></header><div class="search-lab-body">${body}</div></section>`;
  const number=(id,title,value,min,max,step='1')=>`<label for="${id}">${title}<input id="${id}" type="number" value="${value}" min="${min}" max="${max}" step="${step}"></label>`;
  window.renderCourseOverview=({course,saved,escapeHTML:e,main,toc,footer})=>{
    const start=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE SEARCH SYSTEMS GUIDE <span>／ 從找得到，到值得信任</span></div><h1>Search<span class="hero-period">.</span><br><span class="search-hero-line">Beyond similarity.</span></h1><h2 class="hero-subtitle">找到相關的資料，<br>也守住資料的邊界。</h2><p class="hero-description">從第一個全文索引，走進向量資料庫與混合搜尋。理解索引如何建立、資料如何更新，以及查詢如何在品質、速度與一致性之間取捨。</p><div class="hero-meta"><span><b>10</b> 章主線</span><span><b>60</b> 個閱讀單元</span><span><b>32</b> 份 Python 範例</span><span><b>7</b> 個互動實驗</span></div><div class="hero-actions"><a class="primary-button" href="#${start}">${saved.last?'繼續學習':'從搜尋系統開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/experiments">先觀察排名如何改變 ↓</a></div></section>
    <svg class="search-diagram" viewBox="0 0 680 160" role="img" aria-labelledby="search-architecture-title"><title id="search-architecture-title">來源經事件同步全文與向量索引，候選回來源驗證後融合</title><g fill="none" stroke="currentColor"><rect x="2" y="38" width="158" height="74" rx="8"/><rect x="210" y="10" width="190" height="57" rx="8"/><rect x="210" y="87" width="190" height="57" rx="8"/><rect x="448" y="38" width="226" height="74" rx="8"/><path d="M160 75h25V38h25m-25 37v40h25m190-77h24v37h24m-48 40h24V75"/></g><text x="18" y="65">SOURCE + OUTBOX</text><text x="18" y="91" class="diagram-caption">權威資料、版本與變更</text><text x="228" y="34">LEXICAL INDEX</text><text x="228" y="54" class="diagram-caption">詞、位置、欄位</text><text x="228" y="111">VECTOR INDEX</text><text x="228" y="132" class="diagram-caption">距離、候選、資格</text><text x="467" y="65">VERIFY → FUSE</text><text x="467" y="91" class="diagram-caption">回來源檢查，再排序與呈現</text></svg>
    <section id="quick-start"><div class="section-header"><h2>從可執行的最小系統開始</h2><span>BUILD → QUERY → VERIFY</span></div><div class="search-route"><strong>完整主線</strong><p><a href="#03-versions-and-environment">建立環境</a> → <a href="#04-first-fts">第一次全文搜尋</a> → <a href="#20-faiss-flat">Faiss Exact</a> → <a href="#25-collections-and-local">Qdrant Local</a> → <a href="#38-reciprocal-rank-fusion">RRF</a> → <a href="#56-catalog-project">完整商品搜尋</a> → <a href="#57-acceptance-and-delivery">驗收與重建</a>。</p><p>Embedding 課程負責表示與模型，RAG 課程負責證據與答案；這裡深入索引、儲存與維運。<a href="#01-scope-and-overlap">查看課程分工 →</a></p></div></section>
    <section id="roadmap"><div class="section-header"><h2>完整學習路線</h2><span>10 CHAPTERS · 60 UNITS</span></div><div class="module-list">${course.groups.map(g=>{const units=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${units[0].id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${units.length} UNITS ↗</span></a>`;}).join('')}</div></section>
    <section id="experiments"><div class="section-header"><h2>把索引與排名，變成看得見的取捨</h2><span>7 INTERACTIVE LABS</span></div><p class="hero-description">固定資料與教學模擬，全部在瀏覽器計算。實際 SQLite、Faiss 與 Qdrant 引擎請執行 Python 範例。</p>
    ${lab(1,'文字先變成什麼，才決定查得到什麼',`<div class="search-controls"><label for="token-text">輸入文字<input id="token-text" value="USB 向量資料庫" maxlength="160"></label><label for="token-mode">切分方式<select id="token-mode"><option value="words" selected>單詞與連續漢字</option><option value="bigrams">漢字 bigram</option></select></label></div><output id="token-output" aria-live="polite"></output><p class="lab-caption">這是明確的簡易切詞規則，並非成熟中文分詞器，也不是 SQLite 預設 analyzer。</p>`)}
    ${lab(2,'BM25：長文件與重複詞，誰比較占優勢',`<div class="search-controls"><label for="bm-query">查詢<input id="bm-query" value="usb hub" maxlength="80"></label>${number('bm-k1','詞頻飽和 k1',1.2,.1,3,'.1')}${number('bm-b','長度修正 b',.75,0,1,'.05')}</div><div id="bm-ranking" class="score-chart" role="img" aria-label="三篇文件的手算 BM25 分數"></div><p class="lab-caption">固定三篇文件；正值 IDF 版本。數值不等同 SQLite bm25() 或 Elasticsearch 的實際分數。</p>`)}
    ${lab(3,'先取候選再過濾，為什麼可能只剩一筆',`<div class="search-controls">${number('filter-budget','全域候選預算',3,1,8)}</div><pre id="filter-output" aria-live="polite"></pre><p class="lab-caption">A 代表可查文件，B 代表其他租戶；最終 k=3。固定順序模擬候選耗盡，沒有執行 HNSW。</p>`)}
    ${lab(4,'RRF：兩條路線如何取得共識',`<p>文字：[A, B, C]；向量：[C, D, A]。調整向量權重，觀察兩路都出現的文件。</p><div class="search-controls">${number('rrf-c','RRF 常數 c',60,0,100)}${number('rrf-weight','向量分支權重',1,0,3,'.1')}</div><pre id="rrf-output" aria-live="polite"></pre><p class="lab-caption">名次從 1 起算；權重0的分支完全不貢獻。RRF 分數不是相關機率。</p>`)}
    ${lab(5,'來源先更新，索引晚一步：現在能顯示嗎',`<div class="search-buttons"><button id="life-update" class="secondary-button">來源更新</button><button id="life-delete" class="secondary-button">來源刪除</button><button id="life-replay" class="secondary-button">同步 Worker</button><button id="life-old" class="secondary-button">重送舊 v1</button><button id="life-reset" class="secondary-button">重設</button></div><pre id="life-state"></pre><output id="life-output" aria-live="polite"></output><p class="lab-caption">單一有序 worker 的狀態模擬；最新來源資格與版本決定顯示，並非分散式 CAS 實作。</p>`)}
    ${lab(6,'量化省了哪一部分？把容量算完整',`<div class="search-controls">${number('cap-n','向量筆數 N',1000000,1,1e9)}${number('cap-d','維度 d',768,1,100000)}<label for="cap-bits">每元素 bits<select id="cap-bits"><option value="8" selected>8 bits</option><option value="16">16 bits</option><option value="32">32 bits</option></select></label>${number('cap-m','圖參數 M（0忽略圖）',16,0,128)}${number('cap-copies','總份數（含 primary）',2,1,10)}${number('cap-headroom','容量餘裕倍數',1.3,1,5,'.1')}<label class="search-check" for="cap-retain"><input id="cap-retain" type="checkbox" checked>另保留 float32 原向量</label></div><pre id="cap-output" aria-live="polite"></pre><p class="lab-caption">圖用 N×M×2×4 粗估。不含 payload、倒排、WAL、備份、codebook、allocator 與重建暫存；不是總服務 RAM 保證。</p>`)}
    ${lab(7,'ANN Recall、相關性與尾延遲是三件事',`<p>Exact 真值：[A, B, C]；ANN 結果：[A, D, B]，k=3。相關性等級指前三名與其理想重排的比較。</p><div class="search-controls"><label for="metric-grades">前三名 relevance（0–3，以逗號分隔）<input id="metric-grades" value="3,0,1" maxlength="40"></label><label for="metric-times">觀測延遲 ms（逗號分隔）<input id="metric-times" value="10,12,13,14,50" maxlength="200"></label></div><pre id="metric-output" aria-live="polite"></pre><p class="lab-caption">輸入是觀測值練習，沒有在瀏覽器測服務效能。小樣本百分位不穩定；這裡以線性插值計算。</p>`)}
    </section><section id="baseline" class="reading-note"><strong>版本與驗證範圍</strong><p>2026-11-05：SQLite 3.54.1、Elasticsearch 9.5.6、Qdrant 1.20.0、Faiss 1.15.1、PostgreSQL 18.6／pgvector 0.8.7。主線實測本機 FTS5、Faiss 與 Qdrant Local；Elasticsearch 預設記錄 SDK 請求，PostgreSQL 預設檢查 SQL。遠端服務、容器、RLS 與叢集故障需另行驗收。</p><a href="examples/README.md">安裝與32份範例 ↗</a> · <a href="examples.zip" download>下載完整實作 ↓</a> · <a href="#60-reference-and-versions">版本與參考資料 →</a></section>${footer}`;
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於課程</a><a href="#overview/quick-start">快速實作</a><a href="#overview/roadmap">完整目錄</a><a href="#overview/experiments">七個互動實驗</a><a href="#overview/baseline">版本與下載</a></div><div class="toc-tip"><p>先建立真值，再調索引；先檢查資格，再比較名次。</p><p>進度與筆記保存在此瀏覽器。</p></div>`;
    mount(main,e);
  };
  window.renderCourseOverview.courseSlug='search';
  function mount(main,e){
    const q=s=>main.querySelector(s),n=s=>{if(!q(s).value.trim())throw new RangeError('數值欄位不可空白');return Number(q(s).value);},show=(s,text,ok=true)=>{q(s).textContent=text;q(s).dataset.status=ok?'ok':'error';};
    function bind(ids,fn,out){const run=()=>{try{fn();}catch(err){show(out,err.message,false);}};ids.forEach(id=>{q(id).oninput=run;q(id).onchange=run;});run();}
    bind(['#token-text','#token-mode'],()=>show('#token-output',JSON.stringify(analyze(q('#token-text').value,q('#token-mode').value))), '#token-output');
    bind(['#bm-query','#bm-k1','#bm-b'],()=>{const rows=bm25(q('#bm-query').value,n('#bm-k1'),n('#bm-b')),max=Math.max(1e-9,...rows.map(r=>r.score));q('#bm-ranking').innerHTML=rows.map(r=>`<div class="score-row"><strong>${r.id}</strong><div><span>${e(r.text)}</span><div class="score-track"><i style="width:${100*r.score/max}%"></i></div></div><span class="mono">${r.score.toFixed(4)}</span></div>`).join('');q('#bm-ranking').dataset.status='ok';},'#bm-ranking');
    bind(['#filter-budget'],()=>{const r=filtered(n('#filter-budget'));show('#filter-output',`掃描候選：${r.scanned.join(' → ')}\n後過濾：${r.post.join(', ')}（${r.post.length}/3）\n可查集合先界定：${r.eligibleFirst.join(', ')}`);},'#filter-output');
    bind(['#rrf-c','#rrf-weight'],()=>show('#rrf-output',rrf([['A','B','C'],['C','D','A']],n('#rrf-c'),[1,n('#rrf-weight')]).map(r=>`${r.id}  ${r.score.toFixed(6)}`).join('\n')),'#rrf-output');
    let state=lifecycle();const draw=message=>{q('#life-state').textContent=JSON.stringify(state.snapshot(),null,2);show('#life-output',message);};
    for(const action of ['update','delete','replay','old'])q('#life-'+action).onclick=()=>draw(state.action(action));q('#life-reset').onclick=()=>{state=lifecycle();draw('已重設：來源與索引都是 v1。');};draw('來源與索引版本相同，目前可顯示。');
    bind(['#cap-n','#cap-d','#cap-bits','#cap-m','#cap-copies','#cap-headroom','#cap-retain'],()=>{const r=capacity(n('#cap-n'),n('#cap-d'),n('#cap-bits'),n('#cap-m'),n('#cap-copies'),n('#cap-headroom'),q('#cap-retain').checked);show('#cap-output',`表示：${(r.vectors/1e9).toFixed(3)} GB\n保留原向量：${(r.originals/1e9).toFixed(3)} GB\n圖粗估：${(r.graph/1e9).toFixed(3)} GB\n含 copies 與餘裕：${r.GB.toFixed(3)} GB / ${r.GiB.toFixed(3)} GiB`);},'#cap-output');
    bind(['#metric-grades','#metric-times'],()=>{const parse=selector=>q(selector).value.split(',').map(s=>s.trim()===''?NaN:Number(s));const grades=parse('#metric-grades');if(grades.length!==3||grades.some(g=>!Number.isInteger(g)||g<0||g>3))throw new RangeError('請填三個 0–3 整數等級');const r=quality(['A','B','C'],['A','D','B'],grades,parse('#metric-times'));show('#metric-output',`ANN Recall@3：${(r.recall*100).toFixed(1)}%\n這三筆的 nDCG@3：${r.ndcg===null?'不適用':r.ndcg.toFixed(4)}\np50：${r.p50.toFixed(2)} ms\np95：${r.p95.toFixed(2)} ms`);},'#metric-output');
  }
})();
