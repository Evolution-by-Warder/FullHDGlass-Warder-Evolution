# TEST214 — dark background, edge spill cleanup, and Plugin Browser

- Used the owner-provided original 121-image ZIP and approved six-image ZIP as source.
- Set the full canvas background matte to black RGBA alpha 206. Border-connected near-neutral gray spill pixels (RGB maximum ≤ 180 and channel spread ≤ 24) were also reset to black/alpha 206; colored foreground, bright chrome, blue effects and warm lighting were left unchanged. No scaling or redraw of the original 121 images.
- Replaced the old gamepad runtime `plugin_selection.png` with a new photorealistic modular software/plugin browser asset, 810×810 RGBA.
- Both runtime ZIPs contain 125 unique PNG paths, pass CRC, and all PNGs decode as 810×810 RGBA. Shutdown and standby images are distinct.
- The in-skin `downloads.json` now points to these TEST214 split archives and their SHA-256 digests.
- Package validation cannot confirm rendering on the user's receiver; install/download and receiver display still need to be checked there.
