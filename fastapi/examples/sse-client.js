/* JSON SSE decoder for this service. Supports LF/CRLF and fragmented UTF-8. */
(() => {
  'use strict';
  function createDecoder(onEvent, maxPending=65536){
    if(typeof onEvent!=='function'||!Number.isInteger(maxPending)||maxPending<32||maxPending>65536)throw new RangeError('decoder policy');
    const decoder=new TextDecoder('utf-8',{fatal:true});let pending='',closed=false;
    function consume(){
      let match;
      while((match=pending.match(/\r?\n\r?\n/))){
        const frame=pending.slice(0,match.index);pending=pending.slice(match.index+match[0].length);
        let id=null,event='message';const data=[];
        for(const line of frame.split(/\r?\n/)){
          if(!line||line.startsWith(':'))continue;
          const split=line.indexOf(':'),field=split<0?line:line.slice(0,split),value=split<0?'':line.slice(split+1).replace(/^ /,'');
          if(field==='id'){if(!/^\d{1,15}$/.test(value))throw new Error('invalid event ID');id=value;}
          else if(field==='event'){if(value.length>64||value.includes('\0'))throw new Error('invalid event type');event=value;}
          else if(field==='data')data.push(value);
        }
        if(data.length)onEvent({id,event,data:JSON.parse(data.join('\n'))});
      }
    }
    return Object.freeze({
      feed(bytes){if(closed||!(bytes instanceof Uint8Array))throw new TypeError('open decoder needs bytes');pending+=decoder.decode(bytes,{stream:true});if(pending.length>maxPending)throw new Error('pending event budget exceeded');consume();},
      finish(){if(closed)throw new Error('decoder closed');closed=true;pending+=decoder.decode();consume();if(pending.trim())throw new Error('incomplete event at end of stream');}
    });
  }
  window.RelaySSE=Object.freeze({createDecoder});
})();
