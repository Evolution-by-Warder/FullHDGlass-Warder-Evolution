# OpenATV ServiceListLegacy EPG-field clipping — source-only fix

Status: **source patch verified; native build and GigaBlue receiver test NOT done**.

## Problem and exact receiver context

Warder TEST9 uses native `ServiceListLegacy` and native event-progress
bar/percentage/minutes. This is responsive on GigaBlue Quad 4K Pro with
OpenATV 8.1 beta, but long EPG labels draw through the right-hand
progress indicator. `fieldMargins` only reserves space; legacy
`eListboxServiceContent::paint` calls `painter.renderPara` for EPG text
without clipping to the individual service-info field.

The reported Enigma2 package was:
`8.1.0~beta+git36096+f9f72e10+f9f72e1115-r1`.
Public OpenATV source commit **f9f72e11152cab6cd4cadccf412cf7013370fc4a**
is available. Its C++ legacy painter was checked; this is a source
reference, NOT proof of the precise downstream build configuration.

## Fix

`tools/apply-native-servicelist-clip.py` narrowly brackets the existing
`painter.renderPara` call in a `painter.clip(eventClip)` /
`painter.clippop()` pair **only when `e == celServiceInfo`**. The clip
uses the native service-info text rectangle, capped before the adjacent
right-hand progressbar / percent / minutes cell, with the original
`m_items_distances` gap. Left-hand progress indicators and no indicator
retain their own native service-info rectangle.

No new progressbar, EPG lookup, bitmap, canvas, black mask, extra timer or
picon handling is introduced. For very long native titles the remaining
letters are visually clipped (no promised ellipsis or marquee).

## Proven / not proven

- CI fetches exact upstream source commit and applies the patch.
- Source diff whitespace check and focused source tests pass.
- Source comparison confirms the actual native progressbar painter,
  EPG event retrieval and non-service-info text render paths are untouched.
- A ZIP containing the generated C++ diff, provenance and checksums is
  uploaded as **openatv-native-epg-clip-SOURCE-ONLY**.
- **NO ARMv7 native enigma2 compile**, image integration, actual receipt of
  signed firmware, screenshot acceptance or real box install has been done.
- **NO skin IPK can carry this native C++ change**. TEST9 remains as-is,
  with the text overlap, until rebuilt firmware implements it.

## Safe deployment requirements

Use a trusted OpenATV/OE-Alliance environment pinned to the receiver
compatible MACHINE, DISTRO, source commit and native dependencies.
Run the normal BitBake Enigma2 recipe with this patch; do not overwrite
`/usr/bin/enigma2` or manually install a guessed `enigma2` IPK.
Test native bar/percentage/minutes LEFT/RIGHT/NO mode, picon text spacing,
selected/unselected rows, long Unicode text, large fonts, scrolling,
different bouquets and all relevant ChannelSelection/PIG screens on a
recovery-capable receiver. Only publish after passing native visual QA.

An alternative without any firmware rebuild is to adopt OpenATV's modern
`ServiceList` with a purpose-built MultiContent template, but that is
not a drop-in replacement for Warder's legacy widget and requires its own
layout/compatibility design and receiver testing. Do not force this global
switch silently for users.
