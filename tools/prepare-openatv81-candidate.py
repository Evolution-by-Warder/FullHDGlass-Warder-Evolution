#!/usr/bin/env python3
"""Stage the approved helper bytes for the isolated list row clipping test."""
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('approved_bitrate_assets',ROOT/'tools/prepare-bitrate-stable-release.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.VERSION='1.0.60-test2'
module.main()
