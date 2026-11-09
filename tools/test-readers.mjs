/* Development QA: requires local .qa/vendor DOM, parser and KaTeX modules.
 * Separate workers prevent CommonJS script caching or browser-global state from
 * letting one course's reader initialization stand in for another course's test.
 * These are DOM tests, not real-browser visual tests. */
import {Worker,isMainThread,parentPort,workerData} from 'node:worker_threads';

export const reports=[];
if(isMainThread) {
  for(const file of ['test-reader.mjs','test-llm-reader.mjs','test-rag-reader.mjs','test-embedding-reader.mjs','test-pytorch-reader.mjs','test-machine-learning-reader.mjs','test-deep-learning-reader.mjs','test-statistics-reader.mjs','test-mcp-reader.mjs','test-search-reader.mjs','test-economics-reader.mjs','test-nutrition-reader.mjs','test-exercise-reader.mjs','test-reader-numbering.mjs']) {
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
  const {verifyReaderNumbering}=await import('./check-reader-numbering.mjs');
  parentPort.postMessage({...result.report,numbering:verifyReaderNumbering()});
}
