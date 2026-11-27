/* Loopback-only demo; tokens are never persisted or placed in URLs. */
(() => {
  'use strict';
  const q=id=>document.getElementById(id);
  let documentId=null,jobId=null,cursor=0,controller=null;
  const show=value=>{q('output').textContent=JSON.stringify(value,null,2).slice(0,64000);};
  function base(){const url=new URL(q('base').value);if(url.protocol!=='http:'||!['127.0.0.1','localhost'].includes(url.hostname)||url.username||url.password||url.pathname!=='/'||url.search||url.hash)throw new Error('本範例只允許http本機API根網址');return url.origin;}
  async function request(path,options={}){const token=q('token').value.trim();if(!token)throw new Error('請先貼入本機佈建token');const response=await fetch(base()+path,{...options,headers:{Authorization:'Bearer '+token,...options.headers}});if(!response.ok){const body=await response.text();throw new Error(`HTTP ${response.status}: ${body.slice(0,2000)}`);}return response;}
  function bind(id,fn){q(id).addEventListener('click',()=>Promise.resolve().then(fn).catch(error=>{if(error.name!=='AbortError')q('state').textContent=error.message;}));}
  q('token').addEventListener('input',()=>{controller?.abort();documentId=jobId=null;cursor=0;q('output').textContent='';q('state').textContent='身分已改變，先前工作與游標已清除。';});
  bind('upload',async()=>{const response=await request('/api/v1/documents',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:'Browser policy',text:q('document').value})});const result=await response.json();documentId=result.id;jobId=null;cursor=0;show(result);q('state').textContent='文件已建立。';});
  bind('submit',async()=>{if(!documentId)throw new Error('請先建立文件');const response=await request('/api/v1/jobs',{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':q('key').value},body:JSON.stringify({question:q('question').value,document_ids:[documentId]})});const result=await response.json();if(jobId!==result.id)cursor=0;jobId=result.id;show(result);q('state').textContent='工作已接受；請確認worker正在執行。';});
  bind('inspect',async()=>{if(!jobId)throw new Error('請先提交工作');show(await (await request('/api/v1/jobs/'+jobId)).json());});
  bind('cancel',async()=>{if(!jobId)throw new Error('請先提交工作');show(await (await request('/api/v1/jobs/'+jobId+'/cancel',{method:'POST'})).json());});
  bind('stop',()=>{controller?.abort();q('state').textContent='訂閱停止；持久化工作仍依其狀態執行。';});
  bind('stream',async()=>{if(!jobId)throw new Error('請先提交工作');controller?.abort();const current=new AbortController();controller=current;const currentJob=jobId;const response=await request('/api/v1/jobs/'+currentJob+'/events',{signal:current.signal,headers:{'Last-Event-ID':String(cursor)}});if(!response.headers.get('content-type')?.startsWith('text/event-stream'))throw new Error('非預期串流格式');const reader=response.body.getReader();let rendered=0;
    const decoder=window.RelaySSE.createDecoder(entry=>{if(entry.id&&Number(entry.id)<=cursor)return;const text=JSON.stringify(entry)+'\n';rendered+=text.length;if(rendered>64000)throw new Error('本頁顯示預算已到，請重新連線續讀');q('output').textContent+=text;if(entry.id)cursor=Number(entry.id);});
    q('output').textContent='';try{while(true){const {done,value}=await reader.read();if(done)break;if(jobId!==currentJob)throw new Error('工作已切換');decoder.feed(value);}decoder.finish();q('state').textContent='本次訂閱結束，可帶目前游標繼續回放。';}finally{await reader.cancel().catch(()=>{});reader.releaseLock();if(controller===current)controller=null;}});
})();
