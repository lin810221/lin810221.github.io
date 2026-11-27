"""Optional FFmpeg single-frame extraction; plan only unless --run is explicit."""
from pathlib import Path
import argparse,json,math,shutil,subprocess

def plan(source,target,timestamp,executable='ffmpeg'):
    source,target=Path(source).resolve(),Path(target).resolve()
    if not source.is_file() or source==target or target.exists():raise ValueError('Existing input and a new output path required')
    if not math.isfinite(timestamp) or not 0<=timestamp<=3600:raise ValueError('Timestamp outside lab budget')
    if target.suffix.lower()!='.png':raise ValueError('Output must be PNG')
    return [str(executable),'-nostdin','-v','error','-ss',str(timestamp),'-i',str(source),'-frames:v','1','-vf','scale=1280:720:force_original_aspect_ratio=decrease','-n',str(target)]
def execute(command,run=False):
    if not run:raise RuntimeError('Explicit --run required before starting FFmpeg')
    executable=shutil.which(command[0])
    if not executable:raise RuntimeError('Install an approved FFmpeg build or pass its executable path')
    output=Path(command[-1]);output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([executable,*command[1:]],check=True,timeout=30,stdin=subprocess.DEVNULL,capture_output=True)
    if not output.is_file():raise RuntimeError('No output frame')
    return {'file':str(output),'requested_timestamp_seconds':float(command[5]),'notice':'Requested seek time is not an independently verified source-frame PTS; inspect timing for exact event localization.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--timestamp',type=float,required=True);p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--run',action='store_true');a=p.parse_args();cmd=plan(a.input,a.output,a.timestamp,a.ffmpeg)
    print(json.dumps(execute(cmd,True) if a.run else {'mode':'dry-run; no subprocess started','arguments':cmd},ensure_ascii=False,indent=2))
