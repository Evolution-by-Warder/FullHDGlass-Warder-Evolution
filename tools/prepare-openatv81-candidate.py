#!/usr/bin/env python3
"""Stage approved helper bytes for the isolated OpenATV 8.1 receiver test."""
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('approved_bitrate_assets',ROOT/'tools/prepare-bitrate-stable-release.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.VERSION='1.0.57'
module.main()
