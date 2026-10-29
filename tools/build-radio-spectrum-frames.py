#!/usr/bin/env python3
"""Bake the approved 3px spectrum offline; Pillow is NOT a receiver dependency."""
from math import ceil, exp, pi, sin
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'usr/share/enigma2/hd_glass17/warder-spectrum'
DEST = ROOT / 'source/package-root' / PREFIX
COUNT = 48


class Motion:
    """The TEST1 independent 110ms targets and eased 50ms motion, build-only."""
    def __init__(self):
        self.levels = [2] * 84
        self.peaks = [2] * 84
        self.holds = [0] * 84
        self.visible = [2.0] * 84
        self.visible_peaks = [2.0] * 84
        self.seeds = [((i + 1) * 1103515245 + 12345) & 0x7fffffff for i in range(84)]
        self.targets = [3 + (v % 28) for v in self.seeds]
        self.wait = [i % 4 for i in range(84)]
        self.elapsed = self.time = 0.0
        self.palette = []
        for hue in range(360):
            c = (1.0 - abs(2.0 * .555 - 1.0)) * .88
            s = c * (1.0 - abs((hue / 60.0) % 2.0 - 1.0))
            o = .555 - c / 2.0
            rgb = ((c,s,0),(s,c,0),(0,c,s),(0,s,c),(s,0,c),(c,0,s))[hue//60]
            self.palette.append(tuple(int((v+o)*255) for v in rgb) + (255,))

    def advance(self):
        for i in range(84):
            if self.wait[i] > 0:
                self.wait[i] -= 1
            elif self.levels[i] == self.targets[i]:
                seed = (self.seeds[i]*1103515245+12345+i*97) & 0x7fffffff
                self.seeds[i] = seed
                self.targets[i] = max(3,min(30,3+(((seed>>8)%28+(seed>>17)%28)//2)))
                self.wait[i] = (seed>>5)%4
            target, current = self.targets[i], self.levels[i]
            if target > current:
                current = min(target,current+2+((self.seeds[i]>>3)%3))
            else:
                current = max(target,current-1-((self.seeds[i]>>6)%2))
            self.levels[i] = current
            if current >= self.peaks[i]:
                self.peaks[i], self.holds[i] = current, 2
            elif self.holds[i] > 0:
                self.holds[i] -= 1
            else:
                self.peaks[i] = max(current,self.peaks[i]-1)

    def tick(self):
        self.elapsed += .05
        self.time += .05
        while self.elapsed >= .11:
            self.advance()
            self.elapsed -= .11
        for i in range(84):
            rate = 22.0 if self.levels[i] > self.visible[i] else 15.0
            self.visible[i] += (self.levels[i]-self.visible[i])*(1.0-exp(-rate*.05))
            self.visible_peaks[i] += (self.peaks[i]-self.visible_peaks[i])*(1.0-exp(-18.0*.05))

    def color(self, step, index, level, flow):
        fraction = max(0.0,min(1.0,step/max(1.0,level-1.0)))
        detail = 5.0*sin(self.time*.37+fraction*pi+index*.04)
        return self.palette[int(238.0*(1.0-fraction)+flow+detail)%360]

    def image(self):
        image = Image.new('RGBA',(350,126),(0,0,0,0))
        draw = ImageDraw.Draw(image)
        for i in range(84):
            level = self.visible[i]
            x = 7+i*4
            flow = 13.0*sin(self.time*.65-i*.105)
            for step in range(int(ceil(level))):
                height = int(2*min(1.0,level-step)+.5)
                y = 121-(step+1)*3+2-height
                if height:
                    draw.rectangle((x,y,x+2,y+height-1),fill=self.color(step,i,level,flow))
            peak = self.visible_peaks[i]
            y = int(round(121-(peak+1.0)*3))
            draw.rectangle((x,y,x+2,y+1),fill=self.color(peak,i,peak+1.0,flow))
        return image


def build():
    DEST.mkdir(parents=True,exist_ok=True)
    motion = Motion()
    for _ in range(120): motion.tick()
    assets = []
    for i in range(COUNT):
        for _ in range(2): motion.tick()
        path = DEST / ('frame-%02d.png' % i)
        motion.image().save(path,optimize=True)
        assets.append({'path':PREFIX+'/'+path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {'schema':1,'frames':COUNT,'size':[350,126],'columns':84,'column_width':3,'gap':1,
                'interval_ms':100,'decoded_rgba_bytes_max':350*126*4*COUNT,
                'playback':'forward then reverse, no repeated endpoints; adjacent frames at loop boundary',
                'assets':assets}
    (ROOT/'design/radio-spectrum/frames.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Baked',COUNT,'frames; shared RGBA pixel budget',manifest['decoded_rgba_bytes_max'],'bytes')


if __name__ == '__main__': build()
