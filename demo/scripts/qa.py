"""Check the encoded MP4 and extract its actual frames for independent visual QA."""
import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('output',type=Path);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
def run(args): return subprocess.run(args,check=True,capture_output=True,text=True)
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(a.video)]).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video');sound=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['pix_fmt'],v['width'],v['height'],v['r_frame_rate'],v['nb_read_frames'])==('h264','yuv420p',1080,1080,'30/1','862')
assert sound['codec_name']=='aac' and sound['sample_rate']=='48000'
assert a.video.stat().st_size<15_000_000 and 25<float(probe['format']['duration'])<32
result=run(['ffmpeg','-v','error','-i',str(a.video),'-f','null','-'])
loud=run(['ffmpeg','-hide_banner','-i',str(a.video),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-']).stderr
levels=json.JSONDecoder().raw_decode(loud[loud.rfind('{'):])[0];assert float(levels['input_tp'])<0
atoms=[]
with a.video.open('rb') as f:
    while True:
        head=f.read(8)
        if len(head)<8: break
        size,kind=struct.unpack('>I4s',head);atoms.append(kind.decode())
        assert size>=8;f.seek(size-8,1)
assert atoms.index('moov')<atoms.index('mdat')
frames=[]
for t in [1.6,5.1,9.7,15.3,19.3,22.6,27.3]:
    path=a.output/f'encoded-{t:04.1f}.jpg'
    run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(a.video),'-frames:v','1','-q:v','2',str(path)])
    frames.append(path)
run(['ffmpeg','-v','error','-y','-i',str(a.video),'-vf','fps=1,scale=216:216','-q:v','3',str(a.output/'second-%02d.jpg')])
sheet=Image.new('RGB',(1080,6*244),'#F2F0E8');d=ImageDraw.Draw(sheet)
for i,path in enumerate(sorted(a.output.glob('second-*.jpg'))):
    x=(i%5)*216;y=(i//5)*244;sheet.paste(Image.open(path),(x,y));d.text((x+8,y+221),f'{i}s',fill='#172E37')
sheet.save(a.output/'contact-sheet.jpg',quality=93)
report=dict(video=a.video.name,sha256=hashlib.sha256(a.video.read_bytes()).hexdigest(),sizeBytes=a.video.stat().st_size,duration=probe['format']['duration'],videoStream=v,audioStream=sound,atoms=atoms,fullDecodeExitCode=result.returncode,fullDecodeStderr=result.stderr,loudness=levels,frames=[f.name for f in frames],limits='Numerical audio checks only; no claim of listening. Still-frame visual review cannot prove motion or audio.')
(a.output/'encoded-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['sha256','sizeBytes','duration','atoms','loudness']}))
