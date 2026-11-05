#!/usr/bin/env python3
"""Run both actual selector callbacks and preserve stored SATLIST row identities."""
import ast
import copy
import importlib
import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
package = ModuleType('selector_presentation_test')
package.__path__ = [str(PKG)]
sys.modules[package.__name__] = package
radio = importlib.import_module(package.__name__ + '.warderRadio')
spec = importlib.util.spec_from_file_location('selector_native_sync', PKG / 'warderPiconSync.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
tree = ast.parse((PKG / 'plugin.py').read_text())
table = next(n for n in ast.parse((PKG / 'txt.py').read_text()).body
             if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SATLIST' for t in n.targets))

for legacy in (False, True):
    scope = {'L': legacy}
    exec(compile(ast.Module(body=[table], type_ignores=[]), 'actual-SATLIST', 'exec'), scope)
    rows = scope['SATLIST']
    unchanged = copy.deepcopy(rows)
    indices = sync.task_satlist_display_order(rows)
    ids = [rows[i][2] for i in indices]
    assert ids.index('450W') < ids.index('345W') < ids.index('300W')
    assert ids.index('460E') < ids.index('500E') < ids.index('515E')
    orbits = [int(rows[i][1], 16) for i in indices if rows[i][1] and rows[i][1] != 'EEEE']
    signed = [o - 3600 if o > 1800 else o for o in orbits]
    assert signed == sorted(signed)
    assert indices[0] == next(i for i, r in enumerate(rows) if r[2] == 'EEE')
    assert sorted(indices) == list(range(len(rows))) and rows == unchanged
    for name in ('warderPositionSelectorScr', 'satSelectorScr'):
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)
        method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'startSelect')
        config = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par39=SimpleNamespace(value='/picons'))))
        scope = dict(warderPiconSync=sync, warderRadio=radio, SATLIST=rows, os=os,
                     PLUGINPATH=str(PKG) + '/', SKINPATH='/skin/', config=config)
        exec(compile(ast.Module(body=[method], type_ignores=[]), 'actual-selector-callback', 'exec'), scope)
        rendered = []
        screen = SimpleNamespace(selected={'345W', '500E'}, delP=1,
                                 list=SimpleNamespace(addSelection=lambda *entry: rendered.append(entry)))
        scope['startSelect'](screen)
        if name == 'warderPositionSelectorScr':
            actual_ids = [entry[1]['package_selector'] for entry in rendered]
            assert actual_ids[:3] == ['IPTV-SK-CZ', 'DAB', 'DVB-T-SK-CZ']
            assert actual_ids.index('450W') < actual_ids.index('345W') < actual_ids.index('300W')
            assert actual_ids.index('460E') < actual_ids.index('500E') < actual_ids.index('515E')
            for selector in ('345W', '500E'):
                entry = next(e for e in rendered if e[1]['package_selector'] == selector)
                old_index = next(i for i, r in enumerate(rows) if r[2] == selector)
                assert entry[2] == old_index + 1 and entry[3] is True
                assert entry[1] == sync.task_binding_for_package_selector(selector)
        else:
            assert [entry[2] for entry in rendered] == [i for i in indices if rows[i][1]]
            for entry in rendered:
                assert entry[1] == (rows[entry[2]][0], rows[entry[2]][1])
    assert rows == unchanged
print('PASS: both actual selector callbacks sorted from west to east; stored row IDs, bindings and checked selections preserved in both locale modes')
