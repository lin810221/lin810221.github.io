"""Real WAV/GIF processing; transcript entries are explicitly authored fixtures."""
import wave,math
from PIL import Image,ImageSequence

def audio_info(path):
    with wave.open(str(path),'rb') as f:
        frames=f.getnframes();rate=f.getframerate()
        return {'channels':f.getnchannels(),'sample_width_bytes':f.getsampwidth(),'sample_rate':rate,'frames':frames,'duration_ms':frames/rate*1000}

def aligned_segments(segments,duration_ms):
    previous=0
    for s in segments:
        if any(type(s[k]) is not int for k in ('start_ms','end_ms')) or not previous<=s['start_ms']<s['end_ms']<=duration_ms:raise ValueError('Invalid transcript interval')
        if not isinstance(s['text'],str) or not s['text']:raise ValueError('Missing transcript text')
        previous=s['end_ms']
    return segments

def segment_at(segments,timestamp_ms):
    if not math.isfinite(timestamp_ms) or timestamp_ms<0:raise ValueError('Invalid time')
    return [s for s in segments if s['start_ms']<=timestamp_ms<s['end_ms']]

def gif_frames(path):
    result=[];elapsed=0
    with Image.open(path) as im:
        for i,frame in enumerate(ImageSequence.Iterator(im)):
            duration=frame.info.get('duration',0)
            if duration<=0:raise ValueError('Missing frame timing')
            result.append({'index':i,'start_ms':elapsed,'end_ms':elapsed+duration,'size':frame.size});elapsed+=duration
    return result
