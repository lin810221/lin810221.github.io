"""Optional actual transcription client; dry-run by default, no ASR claim for tones."""
from pathlib import Path
from hashlib import sha256
from urllib.request import Request,urlopen
import argparse,json,os,re,uuid
from media import audio_info

def prepare(path,model):
    path=Path(path);info=audio_info(path)
    if info['duration_ms']>180_000:raise ValueError('This lab allows up to 180 seconds')
    if not re.fullmatch(r'[A-Za-z0-9._:-]+',model):raise ValueError('Explicit supported model required')
    with path.open('rb') as f:raw=f.read(10_000_001)
    if len(raw)>10_000_000:raise ValueError('This lab allows up to 10MB WAV')
    boundary='docweave'+uuid.uuid4().hex
    parts=[]
    for name,value in [('model',model),('response_format','json')]:parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()+raw+f'\r\n--{boundary}--\r\n'.encode())
    return {'url':'https://api.openai.com/v1/audio/transcriptions','content_type':'multipart/form-data; boundary='+boundary,'body':b''.join(parts),'source_sha256':sha256(raw).hexdigest(),'audio':info,'model':model}
def transcribe(spec,live=False):
    if not live:raise RuntimeError('Explicit --live is required before uploading audio')
    key=os.environ.get('OPENAI_API_KEY')
    if not key:raise RuntimeError('Missing OPENAI_API_KEY')
    req=Request(spec['url'],data=spec['body'],headers={'Authorization':'Bearer '+key,'Content-Type':spec['content_type']},method='POST')
    with urlopen(req,timeout=60) as response:raw=response.read(1_000_001)
    if len(raw)>1_000_000:raise ValueError('Response budget exceeded')
    result=json.loads(raw)
    if not isinstance(result,dict) or not isinstance(result.get('text'),str):raise ValueError('Expected JSON transcript text')
    return {'source_sha256':spec['source_sha256'],'model':spec['model'],'response':result,'notice':'Text is a model prediction; timestamps are only available when explicitly supported and returned.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--audio',type=Path,required=True);p.add_argument('--model',required=True);p.add_argument('--live',action='store_true');a=p.parse_args();s=prepare(a.audio,a.model)
    print(json.dumps(transcribe(s,True) if a.live else {'mode':'dry-run; no credential read or upload','url':s['url'],'model':a.model,'audio':s['audio'],'notice':'Bundled tones.wav is not speech. Use an authorized speech sample for actual ASR validation.'},ensure_ascii=False,indent=2))
