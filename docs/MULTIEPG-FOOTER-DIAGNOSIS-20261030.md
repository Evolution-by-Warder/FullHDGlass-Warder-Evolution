# MultiEPG footer diagnosis — 30 October 2026

Status: cause reproduced, diagnostic branch only. Production is unchanged.

The owner supplied a receiver screenshot of GraphicalEPGPIG with all four bottom colour captions absent. The published FullHDGlass 1.0.44 IPK was downloaded and SHA256 checked; its plugin.py and skin.xml exactly match the inspected production source.

The four footer widgets remain present at y=930, height=42 inside the 1050px screen. The failure is in their Python source initialization, not their XML placement.

OpenATV commit [ce3361e](https://github.com/openatv/enigma2/commit/ce3361e87258ca73f2743a088fe502e71fd3485a), dated 24 October 2026, refactored EPG screens/lists/configuration. The graphical guide now uses EPGSelectionGrid. Its compatibility EPGSelection.__new__ returns a Grid instance, so a wrapper placed on the old compatibility EPGSelection.__init__ is not called. The four custom warder_key_* StaticText sources therefore are not initialized.

In addition, the old RefreshColouredKeys method no longer exists. The unguarded attribute lookup in our legacy patch raises AttributeError at plugin.py:1321. Its outer except Exception: pass suppresses that failure and skips the rest of the custom colour-button handler installation.

A targeted harness executes the unchanged production patch with the actual modern OpenATV compatibility metaclass/factory and minimal GUI stand-ins: old interface produces all four captions; new interface produces zero and captures the suppressed AttributeError. This is an interface reproduction, not a physical receiver session. The exact installed OpenATV build on the owner's receiver has not been read.

Required repair: install caption initialization and matching colour actions on the real graphical screen lifecycle for both OpenATV interfaces, guard optional legacy refresh methods independently, retain the one-open Program Info guard, and add a runtime compatibility regression test. Preserve all approved PIG/grid/selection/picon/timeline geometry and unrelated screens. Do not introduce receiver diagnostic files.

Reproduction inputs (official pinned OpenATV sources):

- Before: https://raw.githubusercontent.com/openatv/enigma2/06de0c9cfe7c449f1327dfe7e3f6057448526945/lib/python/Screens/EpgSelection.py — save as EpgSelection-openatv-before.py.
- After: https://raw.githubusercontent.com/openatv/enigma2/f3aa19683fbbe8350b8b6627a341e5581a42eb12/lib/python/Screens/EpgSelection.py — save as EpgSelection-openatv-after.py.

```sh
python tools/diagnose-multiepg-footer.py --snapshots /path/to/snapshots --report /tmp/multiepg-diagnosis.json
```

Machine-readable evidence: reports/multiepg-footer-diagnosis-20261030.json.
