# -*- coding: utf-8 -*-
"""Select only helpers whose reviewed target matches the receiver."""
import json
import os
import re
import sys

LEGACY='/usr/bin/btrGen17'
TARGETS=os.path.join(os.path.dirname(__file__),'warderBitrateTargets.json')

def select_helper(cpu, exists=os.path.isfile, cpuinfo=None, kernel=None, byteorder=None, targets=None):
    if cpu=='arm':
        return '/usr/bin/warder-bitrate-arm'
    if cpu=='aarch64':
        return '/usr/bin/warder-bitrate-aarch64'
    if cpu!='mipsel' or not exists('/usr/bin/warder-bitrate-mipsel'):
        return LEGACY
    try:
        if targets is None:
            with open(TARGETS,'r') as source:targets=json.load(source)
        target=targets['mipsel']
        if target['isa']!='mips32r2' or target['byteorder']!='little':return LEGACY
        if (sys.byteorder if byteorder is None else byteorder)!='little':return LEGACY
        if kernel is None:kernel=os.uname()[2]
        match=re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?',kernel)
        if not match:return LEGACY
        actual=tuple(int(value or 0) for value in match.groups())
        minimum=tuple(target['minimum_kernel'])
        minimum=(minimum+(0,0,0))[:3]
        if minimum<(3,2,0) or actual<minimum:return LEGACY
        if cpuinfo is None:
            with open('/proc/cpuinfo','r') as source:cpuinfo=source.read()
        isa=re.search(r'^\s*isa\s*:\s*(.*)$',cpuinfo,re.MULTILINE|re.IGNORECASE)
        words=isa.group(1).lower().split() if isa else []
        if 'mips32r2' not in words or 'mips32r6' in words or 'mips64r6' in words:return LEGACY
        if target['requires_fpu'] and not re.search(r'^cpu model\s*:.*\bFPU\b',cpuinfo,re.MULTILINE|re.IGNORECASE):return LEGACY
        return '/usr/bin/warder-bitrate-mipsel'
    except (OSError,IOError,ValueError,TypeError,KeyError,AttributeError):
        return LEGACY


def external_helper_available(cpu, restricted, exists=os.path.isfile):
    helper=select_helper(cpu,exists=exists)
    return exists(helper) and (helper!=LEGACY or not restricted)

def startup_delay(cpu, native, exists=os.path.isfile):
    if select_helper(cpu,exists=exists)!=LEGACY:return 750
    return 5000 if native else 8000
