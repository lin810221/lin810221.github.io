/* Development QA: requires local .qa/vendor DOM, parser and KaTeX modules.
 * Separate workers prevent CommonJS script caching or browser-global state from
 * letting one course's reader initialization stand in for another course's test.
 * These are DOM tests, not real-browser visual tests. */
import {Worker,isMainThread,parentPort,workerData} from 'node:worker_threads';

export const reports=[];
if(isMainThread) {
  for(const file of ['test-reader.mjs','test-llm-reader.mjs','test-rag-reader.mjs','test-embedding-reader.mjs','test-pytorch-reader.mjs']) {
    reports.push(await new Promise((resolve,reject)=> {
      const worker=new Worker(new URL(import.meta.url),{workerData:file});
      let result;
      worker.on('message',message=>{result=message;});
      worker.on('error',reject);
      worker.on('exit',code=>code===0&&result?resolve(result):reject(new Error(`${file} exited ${code}`)));
    }));
  }
} else {
  const result=await import(new URL(workerData,import.meta.url));
  parentPort.postMessage(result.report);
}
