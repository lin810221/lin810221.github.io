/* Browser-only teaching simulations. No model, MCP or external network calls. */
(() => {
  'use strict';
  function validateSearch(raw){
    let value;try{value=JSON.parse(raw);}catch{return {ok:false,message:'JSON 格式不正確。'};}
    if(!value||Array.isArray(value)||typeof value!=='object')return {ok:false,message:'輸入必須是 object。'};
    if(Object.keys(value).some(key=>!['query','limit'].includes(key)))return {ok:false,message:'此封閉 Schema 不接受額外欄位。'};
    if(typeof value.query!=='string'||!value.query.trim()||value.query.length>100)return {ok:false,message:'query 必須是 1–100 字元的非空白字串。'};
    const limit=value.limit===undefined?5:value.limit;
    if(!Number.isInteger(limit)||limit<1||limit>10)return {ok:false,message:'limit 必須是 1–10 的整數，不能是字串或布林值。'};
    return {ok:true,value:{query:value.query,limit},message:'契約通過，可以進入身分與業務條件檢查。'};
  }
  function authorize({tenant,owner,scopes,expired,action}){
    if(expired)return {ok:false,message:'拒絕：Token 已過期，不能進入工具。'};
    const required=action==='write'?'tickets:write':'tickets:read';
    if(!scopes.includes(required))return {ok:false,message:`拒絕：缺少 ${required}。`};
    if(tenant!==owner)return {ok:false,message:'拒絕：工單不屬於目前主體的租戶。'};
    return {ok:true,message:action==='write'?'權限符合；真正寫入仍需預覽、核准與版本檢查。':'允許讀取此租戶的工單。'};
  }
  function retryPlan(kind,budget,timeout){
    if(!Number.isFinite(budget)||budget<=0||!Number.isFinite(timeout)||timeout<=0)throw new RangeError('正數時間預算才有效');
    const limit=kind==='write-unsafe'?1:3,rows=[];let remaining=budget,spent=0;
    for(let i=0;i<limit&&remaining>1e-9;i++){
      const wait=Math.min(timeout,remaining);rows.push({attempt:i+1,timeout:Number(wait.toFixed(3))});remaining-=wait;spent+=wait;
      if(i+1<limit&&remaining>0){const backoff=Math.min(.1*2**i,remaining);remaining-=backoff;spent+=backoff;}
    }
    return {rows,spent:Number(spent.toFixed(3)),message:kind==='write-unsafe'?'此寫入沒有冪等契約：只安排一次。逾時後先查操作結果。':'僅對可重試的暫時失敗安排後續嘗試，總時間包含 backoff。'};
  }
  function makeApproval(){
    let state='idle',version=1,previewVersion=null,effects=0,receiptKey=null;
    return {snapshot:()=>({state,version,previewVersion,effects}),
      preview(){if(effects)return {ok:false,message:'工單已結案，請重設實驗。'};state='pending';previewVersion=version;return {ok:true,message:'已保存預覽：T1，open → closed；等待可信審核者。'};},
      approve(){if(state!=='pending')return {ok:false,message:'只有 pending 預覽可以核准。'};state='approved';return {ok:true,message:'審核者已核准這份具體預覽。'};},
      change(){version++;return {ok:true,message:'另一個操作者更新了工單，現有預覽可能已過期。'};},
      commit(key){if(!key)return {ok:false,message:'需要冪等鍵。'};if(receiptKey){return receiptKey===key?{ok:true,message:'回傳原收據；沒有再次執行。'}:{ok:false,message:'此預覽已使用，不能換鍵重做。'};}
        if(state!=='approved')return {ok:false,message:'拒絕：尚未取得有效核准。'};
        if(previewVersion!==version)return {ok:false,message:'拒絕：工單版本改變，請重新預覽與核准。'};
        state='consumed';effects++;version++;receiptKey=key;return {ok:true,message:'交易完成，工單已結案，收據已保存。'};}
    };
  }
  window.MCPLab=Object.freeze({validateSearch,authorize,retryPlan,makeApproval});
  const lab=(n,title,body)=>`<section class="mcp-lab" id="mcp-lab-${n}"><header><span class="mono">LAB ${String(n).padStart(2,'0')}</span><h3>${title}</h3></header><div class="mcp-lab-body">${body}</div></section>`;
  window.renderCourseOverview=({course,saved,escapeHTML:e,main,toc,footer})=>{
    const start=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE MODEL CONTEXT PROTOCOL GUIDE <span>／ 讓能力，成為可以信任的介面</span></div><h1>MCP<span class="hero-period">.</span></h1><h2 class="hero-subtitle">從一句需求，<br>走到可驗證的執行。</h2><p class="hero-description">從 Host、Client 與 Server 開始，親手建立工具、資源與 Agent。再走進授權、審核、交易與部署，讓每一次呼叫都有清楚的契約。</p><div class="hero-meta"><span><b>9</b> 章主線</span><span><b>54</b> 個閱讀單元</span><span><b>30</b> 份 Python 範例</span><span><b>6</b> 個互動實驗</span></div><div class="hero-actions"><a class="primary-button" href="#${start}">${saved.last?'繼續學習':'從第一單元開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/experiments">先動手看工具如何執行 ↓</a></div></section>
    <svg class="mcp-diagram" viewBox="0 0 670 125" role="img" aria-labelledby="mcp-architecture-title"><title id="mcp-architecture-title">Host 管理模型與政策，Client 連接 MCP Server，Server 提供受控能力</title><g fill="none" stroke="currentColor"><rect x="2" y="12" width="206" height="75" rx="7"/><rect x="242" y="12" width="143" height="75" rx="7"/><rect x="420" y="12" width="245" height="75" rx="7"/><path d="M208 49h34m143 0h35m-12-5 12 5-12 5"/></g><text x="22" y="39">HOST</text><text x="22" y="65" class="diagram-caption">模型、對話、工具政策</text><text x="260" y="39">CLIENT</text><text x="260" y="65" class="diagram-caption">探索與請求</text><text x="438" y="39">MCP SERVER</text><text x="438" y="65" class="diagram-caption">工具、資源、業務權限</text><text x="2" y="115" class="diagram-caption">DISCOVER → VALIDATE → REVIEW → EXECUTE → VERIFY</text></svg>
    <section id="quick-start"><div class="section-header"><h2>第一條實作路線</h2><span>START SMALL, VERIFY EVERY STEP</span></div><div class="mcp-quickroute"><strong>第一次接觸 MCP？</strong><br>先讀 <a href="#01-why-mcp">它解決什麼</a> → <a href="#04-versions-and-migration">版本差異</a> → <a href="#05-first-server">第一個 Server</a> → <a href="#06-first-client">Client</a> → <a href="#09-stdio">stdio</a> → <a href="#10-streamable-http">HTTP</a>，再完成 <a href="#47-capstone-project">工單專題</a>。<br>閱讀網頁不需安裝套件；執行 Python 範例才需要隔離環境。預設不呼叫模型 API。</div></section>
    <section id="roadmap"><div class="section-header"><h2>完整學習路線</h2><span>9 CHAPTERS · 54 UNITS</span></div><div class="module-list">${course.groups.map(group=>{const units=course.lessons.filter(l=>l.group===group.id);return `<a class="module-row" href="#${units[0].id}"><span class="module-num">${group.number}</span><div><div class="module-name">${e(group.title)}</div><div class="module-description">${e(group.description)}</div></div><span class="module-count">${units.length} UNITS <span aria-hidden="true">↗</span></span></a>`;}).join('')}</div></section>
    <section id="experiments"><div class="section-header"><h2>把抽象協定，變成可觀察的結果</h2><span>6 INTERACTIVE LABS</span></div><p class="hero-description">以下使用固定資料在瀏覽器模擬，不會連線工具、讀取你的檔案或呼叫模型服務。</p>
    ${lab(1,'走過一次協定請求',`<p>比較新版探索與舊版握手。每一步都能看到資料如何送出，版本不同，流程也不同。</p><div class="mcp-controls"><label for="flow-era">協定模式<select id="flow-era"><option value="modern" selected>2026-07-28 · 現代</option><option value="legacy">2025-11-25 · 舊版</option></select></label></div><div class="mcp-flow" id="flow-track"></div><output class="mcp-output" id="flow-step" aria-live="polite"></output><pre id="flow-message"></pre><div class="mcp-buttons"><button class="secondary-button" id="flow-next">下一步 →</button><button class="secondary-button" id="flow-reset">重新觀察</button></div>`)}
    ${lab(2,'把輸入放進契約',`<p>本實驗使用封閉 Schema：query 是非空白字串；limit 是 1–10 的整數。試試字串數字、布林值或額外欄位。</p><label class="field-label" for="schema-input">工具輸入 JSON</label><textarea id="schema-input" spellcheck="false">{"query":"MCP","limit":2}</textarea><div class="mcp-buttons"><button class="secondary-button" id="schema-run">驗證輸入</button></div><output class="mcp-output" id="schema-output" aria-live="polite"></output>`)}
    ${lab(3,'分辨沒有資料與執行失敗',`<p>HTTP 請求成功並不代表工具成功。選一種結果，觀察 Host 應如何處理。</p><div class="mcp-controls"><label for="result-kind">回傳情境<select id="result-kind"><option value="success" selected>成功且有資料</option><option value="empty">成功但沒有命中</option><option value="tool-error">工具執行失敗</option><option value="protocol-error">JSON-RPC 請求失敗</option></select></label></div><pre id="result-message"></pre><output class="mcp-output" id="result-action" aria-live="polite"></output>`)}
    ${lab(4,'檢查主體、Scope 與資料租戶',`<p>此處只模擬身分與 ACL；符合寫入權限之後，仍需檢查具體審核與版本。</p><div class="mcp-controls"><label for="auth-tenant">主體租戶<select id="auth-tenant"><option value="alpha" selected>alpha</option><option value="beta">beta</option></select></label><label for="auth-owner">工單租戶<select id="auth-owner"><option value="alpha" selected>alpha</option><option value="beta">beta</option></select></label><label for="auth-scope">已驗證的 Scopes<select id="auth-scope"><option value="read" selected>tickets:read</option><option value="write">read + write</option></select></label><label for="auth-action">欲執行操作<select id="auth-action"><option value="read" selected>讀取</option><option value="write">寫入</option></select></label><label class="check-label" for="auth-expired"><input type="checkbox" id="auth-expired">Token 已過期</label></div><output class="mcp-output" id="auth-output" aria-live="polite"></output>`)}
    ${lab(5,'核准的是這份預覽，重送的是同一操作',`<p>先預覽，再以審核者核准，最後提交。試試尚未核准就執行、更新工單版本，以及使用同一鍵重送。</p><div class="mcp-controls"><label for="approval-key">冪等鍵<input id="approval-key" value="close-T1-001" maxlength="80"></label></div><div class="mcp-buttons"><button class="secondary-button" id="approval-preview">建立預覽</button><button class="secondary-button" id="approval-review">以審核者核准</button><button class="secondary-button" id="approval-commit">提交／重送</button><button class="secondary-button" id="approval-change">模擬工單更新</button><button class="secondary-button" id="approval-reset">重設</button></div><pre id="approval-state"></pre><output class="mcp-output" id="approval-output" aria-live="polite"></output>`)}
    ${lab(6,'把重試放進時間預算',`<p>這是最壞等待排程模擬，包含 backoff。真正重試還需確認錯誤可恢復與上游冪等契約。</p><div class="mcp-controls"><label for="retry-kind">操作類型<select id="retry-kind"><option value="read" selected>唯讀操作</option><option value="write-safe">有冪等契約的寫入</option><option value="write-unsafe">沒有冪等契約的寫入</option></select></label><label for="retry-budget">總預算（秒）<input type="number" id="retry-budget" value="3" min="0.1" max="30" step="0.1"></label><label for="retry-timeout">單次上限（秒）<input type="number" id="retry-timeout" value="1" min="0.1" max="10" step="0.1"></label></div><pre id="retry-plan"></pre><output class="mcp-output" id="retry-output" aria-live="polite"></output>`)}
    </section><section class="reading-note" id="baseline"><strong>版本與實測範圍</strong><br>2026-11-03 查核：MCP 2026-07-28、官方 Python SDK 2.3.0；本機 Python 3.11.6。範例包含程序內、stdio、loopback HTTP、JWT fixture 與交易測試。三家服務配置未執行付費 API，容器與正式身分服務需另驗證。<br><a href="examples/README.md">安裝、30 份範例與測試說明 ↗</a> · <a href="examples.zip" download>下載完整專案 ↓</a> · <a href="#54-exercises-reference">總練習與版本速查 →</a></section>${footer}`;
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於課程</a><a href="#overview/quick-start">快速上手路線</a><a href="#overview/roadmap">完整目錄</a><a href="#overview/experiments">六個互動實驗</a><a href="#overview/baseline">版本與下載</a></div><div class="toc-tip"><p>先把連線跑通，再驗證契約，最後加入受控變更。</p><p>筆記與進度獨立保存在此瀏覽器。</p></div>`;
    mount(main);
  };
  window.renderCourseOverview.courseSlug='mcp';
  function mount(main){
    const q=s=>main.querySelector(s),report=(selector,result)=>{q(selector).textContent=result.message;q(selector).dataset.status=result.ok===false?'error':'ok';};
    let step=0;
    function drawFlow(){const modern=q('#flow-era').value==='modern',steps=modern?['server/discover','tools/list','tools/call','resultType: complete']:['initialize','notifications/initialized','tools/list','tools/call','CallToolResult'];step=Math.min(step,steps.length-1);
      q('#flow-track').innerHTML=steps.map((s,i)=>`<span class="${i===step?'current':''}">${s}</span>`).join('');q('#flow-step').textContent=`${step+1} / ${steps.length} · ${steps[step]}`;
      const message=step===steps.length-1?{jsonrpc:'2.0',id:step,result:{...(modern?{resultType:'complete'}:{}),content:[{type:'text',text:'Found 2 notes'}],isError:false}}:{jsonrpc:'2.0',...(steps[step].startsWith('notifications/')?{}:{id:step+1}),method:steps[step],params:modern?{_meta:{'io.modelcontextprotocol/protocolVersion':'2026-07-28','io.modelcontextprotocol/clientCapabilities':{}}}:step===0?{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'course-demo',version:'1.0'}}:{}};
      if(steps[step]==='tools/call')Object.assign(message.params,{name:'search_notes',arguments:{query:'MCP'}});
      q('#flow-message').textContent=JSON.stringify(message,null,2);q('#flow-next').disabled=step===steps.length-1;}
    q('#flow-next').onclick=()=>{step++;drawFlow();};q('#flow-reset').onclick=()=>{step=0;drawFlow();};q('#flow-era').onchange=()=>{step=0;drawFlow();};drawFlow();
    q('#schema-run').onclick=()=>report('#schema-output',validateSearch(q('#schema-input').value));q('#schema-run').click();
    function drawResult(){const kind=q('#result-kind').value,payload=kind==='protocol-error'?{jsonrpc:'2.0',id:1,error:{code:-32601,message:'Method not found'}}:{isError:kind==='tool-error',content:[{type:'text',text:kind==='tool-error'?'Ticket unavailable':kind==='empty'?'No matches':'Found 2 notes'}],...(kind==='tool-error'?{}:{structuredContent:{matches:kind==='empty'?[]:['N1','N2']}})};q('#result-message').textContent=JSON.stringify(payload,null,2);report('#result-action',{ok:!kind.endsWith('error'),message:kind==='protocol-error'?'由 Host 處理請求層錯誤；沒有成功工具結果。':kind==='tool-error'?'isError=true：停止讀取成功輸出，依錯誤政策處理。':kind==='empty'?'合法的空結果：可以說沒有命中，不能假裝系統失敗。':'先檢查 isError，再驗證與讀取結構化結果。'});}
    q('#result-kind').onchange=drawResult;drawResult();
    function drawAuth(){report('#auth-output',authorize({tenant:q('#auth-tenant').value,owner:q('#auth-owner').value,scopes:q('#auth-scope').value==='write'?['tickets:read','tickets:write']:['tickets:read'],expired:q('#auth-expired').checked,action:q('#auth-action').value}));}
    for(const id of ['auth-tenant','auth-owner','auth-scope','auth-action','auth-expired'])q('#'+id).onchange=drawAuth;drawAuth();
    let approval=makeApproval();const drawApproval=result=>{q('#approval-state').textContent=JSON.stringify(approval.snapshot(),null,2);report('#approval-output',result);};
    for(const [id,method] of [['approval-preview','preview'],['approval-review','approve'],['approval-change','change']])q('#'+id).onclick=()=>drawApproval(approval[method]());
    q('#approval-commit').onclick=()=>drawApproval(approval.commit(q('#approval-key').value));q('#approval-reset').onclick=()=>{approval=makeApproval();drawApproval({ok:true,message:'請先建立預覽。'});};q('#approval-reset').click();
    function drawRetry(){try{const plan=retryPlan(q('#retry-kind').value,Number(q('#retry-budget').value),Number(q('#retry-timeout').value));q('#retry-plan').textContent=JSON.stringify({attempts:plan.rows,total_wait:plan.spent},null,2);report('#retry-output',{ok:true,message:plan.message});}catch(error){q('#retry-plan').textContent='';report('#retry-output',{ok:false,message:error.message});}}
    for(const id of ['retry-kind','retry-budget','retry-timeout'])q('#'+id).oninput=drawRetry;q('#retry-kind').onchange=drawRetry;drawRetry();
  }
})();
