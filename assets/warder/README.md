# FullHDGlass17 Warder Evolution assets

This tree separates a read-only historical snapshot of the original HDGlass FTP from the clean Warder download layout used by FullHDGlass17 Warder Evolution.

- `archive/original-ftp/` — preserved FTP snapshot, never used directly by the plugin.
- `downloads/picons/` — provider, satellite and CAM graphics.
- `downloads/weather/` — static/alternate/animated weather graphics and info picons.
- `downloads/ui/` — help, menu graphics, ExtraScreens, icon previews and large ChannelSelection graphics.
- `assets-manifest.json` — canonical download paths, sizes and SHA-256 checksums.

The original `skin/` and `skin-vip/` packages are intentionally not copied into the runtime `downloads/` tree. They remain preserved inside the historical FTP snapshot only.
