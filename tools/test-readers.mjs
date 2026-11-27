/* Development QA: requires local .qa/vendor DOM, parser and KaTeX modules.
 * Separate workers prevent CommonJS script caching or browser-global state from
 * letting one course's reader initialization stand in for another course's test.
 * These are DOM tests, not real-browser visual tests. */
import {Worker,isMainThread,parentPort,workerData} from 'node:worker_threads';

export const reports=[];
if(isMainThread) {
  const files=['test-reader.mjs','test-llm-reader.mjs','test-rag-reader.mjs','test-embedding-reader.mjs','test-pytorch-reader.mjs','test-machine-learning-reader.mjs','test-deep-learning-reader.mjs','test-statistics-reader.mjs','test-mcp-reader.mjs','test-search-reader.mjs','test-economics-reader.mjs','test-nutrition-reader.mjs','test-exercise-reader.mjs','test-metabolic-reader.mjs','test-mental-reader.mjs','test-ergo-reader.mjs','test-anatomy-reader.mjs','test-evidence-reader.mjs','test-sleep-reader.mjs','test-public-reader.mjs','test-first-aid-reader.mjs','test-vision-reader.mjs','test-transformer-reader.mjs','test-finetuning-reader.mjs','test-django-reader.mjs','test-sql-reader.mjs','test-multimodal-reader.mjs','test-fastapi-reader.mjs','test-reader-numbering.mjs'];
  for(let offset=0;offset<files.length;offset+=4) {
    reports.push(...await Promise.all(files.slice(offset,offset+4).map(file=>new Promise((resolve,reject)=> {
      const worker=new Worker(new URL(import.meta.url),{workerData:file});
      let result;
      worker.on('message',message=>{result=message;});
      worker.on('error',reject);
      worker.on('exit',code=>code===0&&result?resolve(result):reject(new Error(`${file} exited ${code}`)));
    }))));
  }
} else {
  const result=await import(new URL(workerData,import.meta.url));
  let visuals;
  if(['nutrition','exercise-science','metabolic-health','mental-health','ergonomics'].includes(globalThis.window?.COURSE?.slug)){
    const {verifyHealthVisuals}=await import('./check-health-visuals.mjs');
    visuals=await verifyHealthVisuals();
  }
  const {verifyReaderNumbering}=await import('./check-reader-numbering.mjs');
  parentPort.postMessage({...result.report,...(visuals?{visuals}:{}),numbering:verifyReaderNumbering()});
}
