#!/usr/bin/env python3
"""Replay native Enigma2 Screen.applySkin resolution paths, not GPU painting."""
import argparse
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

parser=argparse.ArgumentParser();parser.add_argument('--upstream',type=Path,required=True)
args,rest=parser.parse_known_args()
tree=ast.parse((args.upstream/'Screens/Screen.py').read_text())
cls=next(node for node in tree.body if isinstance(node,ast.ClassDef) and node.name=='Screen')
method=next(node for node in cls.body if isinstance(node,ast.FunctionDef) and node.name=='applySkin')
namespace={'eWindow':lambda desktop,z:SimpleNamespace(), 'applyAllAttributes':lambda *args:None,'_':lambda value:value}
exec(compile(ast.Module(body=[method],type_ignores=[]),'<native Screen.applySkin>','exec'),namespace)

class ReferenceScaleTests(unittest.TestCase):
    def test_actual_native_method_scales_the_reference_to_every_desktop(self):
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            observed=[]
            screen=SimpleNamespace(desktop=SimpleNamespace(size=lambda:SimpleNamespace(width=lambda:width,height=lambda:height)),
                skinAttributes=[('resolution','1920,1080'),('position','0,0'),('size','1920,1080')],
                instance=None,screenTitle=None,createGUIScreen=lambda *unused:observed.append(screen.scale))
            # OpenPLi reads the GUI desktop globally; OpenATV uses self.desktop.
            namespace.update(getDesktop=lambda unused:screen.desktop, GUI_SKIN_ID=0)
            namespace['applySkin'](screen)
            self.assertEqual(observed,[((width,1920),(height,1080))])

if __name__=='__main__':unittest.main(argv=[__file__]+rest)
