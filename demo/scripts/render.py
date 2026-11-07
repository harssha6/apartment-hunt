"""Render an explicitly editorial workflow film from persisted fictional outputs.
Requires Pillow and ffmpeg. Pass a licensed music file; it is not bundled.
"""
import argparse
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
W = H = 1080
FPS = 30
DURATION = 28.7333333333
CUTS = [0, 3.6369, 7.216, 12.5874, 17.9675, 20.6489, 25.1272, DURATION]
BG, INK, MUTED, TEAL, CORAL, LINE = '#F2F0E8', '#172E37', '#52666D', '#146C60', '#BB4B34', '#D6DBD3'
DATA = json.loads((ROOT/'demo/output/shortlist.json').read_text())
GEO = json.loads((ROOT/'demo/output/shortlist.geojson').read_text())
A, B, C = DATA['listings']

@lru_cache(None)
def font(size, bold=False):
    suffix = 'Arial Bold.ttf' if bold else 'Arial.ttf'
    return ImageFont.truetype(str(ARGS.font_dir/suffix), size)


def text(d, xy, value, size=32, fill=INK, bold=False):
    d.text(xy, value, font=font(size,bold), fill=fill, stroke_width=0)


def box(d, xy, fill='white', outline=None, radius=24):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)


def tag(d, xy, value, color=TEAL):
    x,y=xy; width=d.textlength(value,font=font(25,True))+34
    box(d,(x,y,x+width,y+46),fill=color,radius=10);text(d,(x+17,y+7),value,25,'white',True)


def base(step, heading, sub):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    text(d,(64,40),'APARTMENT HUNT',26,TEAL,True)
    text(d,(64,84),'FICTIONAL INPUTS  /  WORKFLOW VISUALIZATION',22,MUTED)
    text(d,(64,155),heading,65,INK,True)
    text(d,(64,245),sub,30,MUTED)
    for i in range(6):
        d.rounded_rectangle((64+i*160,974,204+i*160,980),radius=3,fill=TEAL if i<step else LINE)
    text(d,(64,1008),'Portable instruction skill  •  Source-backed local files',24,MUTED)
    return im,d


def scene(index, elapsed):
    if index==0:
        im,d=base(1,'Cheap rent. Real cost.','A fictional Padova search. €600/month all-in.')
        text(d,(64,365),'€430',155,INK,True);text(d,(65,540),'+ unknown bills',55,CORAL,True)
        text(d,(66,640),'Can you actually afford it?',44,INK,True)
        d.line((64,735,1016,735),fill=LINE,width=2)
        text(d,(64,780),'Apartment hunting with Grokbot',45,INK,True)
        text(d,(64,850),'Grokbot assisted the original Padova search.',28,MUTED)
        text(d,(64,890),'This demo runs the portable skill on fictional inputs.',28,MUTED)
    elif index==1:
        im,d=base(2,'Give the skill evidence.','Three pasted sources. Private rooms. One budget.')
        for i,r in enumerate([A,B,C]):
            y=325+i*178;box(d,(64,y,1016,y+154));tag(d,(88,y+18),r['title'].upper())
            text(d,(88,y+80),f"€{r['rentMonthly']} rent",41,INK,True)
            bill=f"+ €{r['requiredBillsMonthly']} all bills" if r['requiredBillsMonthly'] is not None else '+ bills extra: amount unstated'
            text(d,(385,y+87),bill,31,CORAL if i==1 else MUTED)
            text(d,(775,y+28),'source / '+r['id'][-1],24,MUTED)
        text(d,(64,886),'$apartment-hunt  →  compare against €600 all-in',31,TEAL,True)
    elif index==2:
        im,d=base(3,'Extract. Keep the gaps.','Every number stays tied to its source quote.')
        box(d,(64,325,1016,530));tag(d,(88,348),'ARCELLA SOURCE / B',CORAL)
        text(d,(88,425),'“Rent EUR 430/month; bills extra”',42,INK,True)
        text(d,(88,482),'No bill amount. No deposit stated.',29,MUTED)
        for j,(label,value,color) in enumerate([('rentMonthly','430',INK),('requiredBillsMonthly','null',CORAL),('allInMonthly','null',CORAL)]):
            y=574+j*94;box(d,(64,y,1016,y+76),fill='#E4E8E0');text(d,(88,y+18),label,31,MUTED);text(d,(806,y+10),value,46,color,True)
        text(d,(64,885),'Unknown ≠ zero. Known minimum: €430.',39,CORAL,True)
    elif index==3:
        im,d=base(4,'Compare the real cost.','Confirmed fits first. Missing bills stay visible.')
        start,end=300,970;scale=(end-start)/700;budget=start+600*scale
        text(d,(budget-85,318),'€600 budget',25,MUTED,True)
        d.line((budget,360,budget,825),fill=MUTED,width=3)
        for i,r in enumerate([A,B,C]):
            y=380+i*151;col=[TEAL,CORAL,CORAL][i]
            text(d,(64,y+4),r['title'],35,INK,True)
            amount=r['knownMonthlyMinimum'];progress=min(1,max(0,elapsed/.6))
            d.rounded_rectangle((start,y+3,start+amount*scale*progress,y+54),radius=9,fill=col)
            label=f"€{amount} all-in" if r['allInMonthly'] is not None else f'€{amount}+  bills unknown'
            text(d,(start,y+67),label,32,col,True)
            if r['allInMonthly'] is None:
                for x in range(int(start+amount*scale)+12,int(budget),20): d.line((x,y+4,x,y+52),fill=CORAL,width=3)
        text(d,(64,885),'€430 + ? cannot outrank €550 confirmed.',39,INK,True)
    elif index==4:
        im,d=base(5,'Persist the shortlist.','shortlist.md  +  shortlist.json  +  shortlist.geojson')
        for i,r in enumerate([A,B,C]):
            y=325+i*132;box(d,(64,y,1016,y+110));text(d,(87,y+17),r['title'],37,INK,True)
            cost=f"€{r['allInMonthly']}" if r['allInMonthly'] is not None else '€430+'
            text(d,(345,y+17),cost,40,INK,True)
            text(d,(565,y+27),r['status'],29,TEAL if i==0 else CORAL,True)
        box(d,(64,765,1016,925),fill=INK)
        text(d,(88,785),'CENTRO  /  MOVE-IN CASH',25,'#AFCBC4',True)
        text(d,(88,830),'€550 first month + €940 deposit',39,'white',True)
        text(d,(88,885),'€1,490 known minimum; one-time fees unstated.',27,'#CEDBD5')
    elif index==5:
        im,d=base(6,'Map only what is supported.','One approximate neighborhood pin. No invented address.')
        box(d,(64,325,1016,760),fill='#DDE5DC')
        # Deliberately schematic: these shapes are graphic decoration, not streets.
        for x in [130,330,550,790,960]: d.line((x,340,x-70,740),fill='#C7D3C9',width=3)
        for y in [410,530,650]: d.line((80,y,1000,y-30),fill='#C7D3C9',width=3)
        d.ellipse((435,428,645,638),fill='#CBDCCD',outline=TEAL,width=2)
        d.ellipse((510,502,570,562),fill=TEAL);d.polygon([(515,548),(565,548),(540,590)],fill=TEAL)
        tag(d,(368,660),'CENTRO / APPROXIMATE')
        text(d,(88,351),'SCHEMATIC • NOT TO SCALE',23,MUTED,True)
        pin=GEO['features'][0];lon,lat=pin['geometry']['coordinates']
        text(d,(64,805),f'{lat}° N, {lon}° E  •  neighborhood precision',33,INK,True)
        text(d,(64,865),'Arcella + Portello: no supported coordinates.',32,MUTED)
        text(d,(64,910),'Source preserved; OpenStreetMap link in GeoJSON.',28,TEAL)
    else:
        im,d=base(6,'Choose with the gaps visible.','Inputs → costs → shortlist → supported map data')
        tag(d,(64,350),'PORTABLE INSTRUCTION SKILL')
        text(d,(64,460),'Apartment hunting',74,INK,True)
        text(d,(64,548),'with Grokbot',74,INK,True)
        text(d,(64,670),'Original Padova workflow: Grokbot-assisted.',31,MUTED)
        text(d,(64,717),'Fictional demo processed now with the portable skill.',29,MUTED)
        box(d,(64,810,1016,916),fill=INK)
        text(d,(87,842),'github.com/harssha6/apartment-hunt',40,'white',True)
    return im


def main():
    ARGS.output.parent.mkdir(parents=True,exist_ok=True)
    command=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1080','-r',str(FPS),'-i','-',
             '-i',str(ARGS.music),'-map','0:v','-map','1:a','-t',str(DURATION),'-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p',
             '-af','loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=in:d=0.08,afade=t=out:st=27.8:d=0.933333',
             '-c:a','aac','-ar','48000','-b:a','160k','-movflags','+faststart',str(ARGS.output)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    for frame in range(round(DURATION*FPS)):
        t=frame/FPS;idx=max(i for i,c in enumerate(CUTS[:-1]) if t>=c)
        im=scene(idx,t-CUTS[idx])
        if idx>0 and t-CUTS[idx]<.16:
            prev=scene(idx-1,CUTS[idx]-CUTS[idx-1]);im=Image.blend(prev,im,(t-CUTS[idx])/.16)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    assert proc.wait()==0, 'ffmpeg encode failed'
    print(ARGS.output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--music',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--font-dir',type=Path,default=Path('/System/Library/Fonts/Supplemental'))
    ARGS=p.parse_args();main()
