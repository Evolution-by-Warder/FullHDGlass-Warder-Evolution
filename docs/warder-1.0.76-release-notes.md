# FullHDGlass – Warder Evolution 1.0.76

## Rendering-engine refinement and adaptive EPG compatibility

Version 1.0.76 introduces a more selective EPG rendering strategy for modern Enigma2 platforms. The enhanced Channel Selection rendering path is enabled only when OpenATV 8.1 runs with an actively detected OpenGL ES (GLES) backend. On other combinations, the skin retains its established native EPG rendering path, minimizing unnecessary work on legacy or framebuffer-based receivers.

The rendering capability check is based on the active graphics backend, rather than simply assuming that GLES is running because the image supports it. Conditional controls keep settings relevant to the current runtime configuration.

## Plugin management interface precision

The package-management screens feature revised geometry for the plugin name, package version and description fields. Independent name/version columns improve the readability of lengthy package identifiers and version strings, while descriptions retain their own full-width second line.

Selected entries now use cyan accents for the name and version and yellow highlighting for the description, with the original unselected-row appearance retained for consistency.

## Refreshed fallback visual identity

New FullHDGlass by Warder artwork updates the skin’s fallback presentation wherever a channel-specific picon is unavailable:

- Coordinated dark and light default picon variants.
- A transparent 220 × 132 fallback for larger picon presentations.
- Refreshed artwork in the Enigma2 skin-selection preview.

The artwork preserves the skin’s recognizable blue-glass visual identity while improving the consistency of different layouts and background styles.

## Compatibility and quality assurance

This update maintains the existing FullHDGlass layout model, service-reference picon lookup behavior, Channel Selection variants, and Prime Time interface. The targeted changes are structured to avoid introducing enhanced rendering on unsupported graphics backends.

Restart the Enigma2 GUI after installation or upgrade so the selected skin resources and renderer settings are applied correctly.

**FullHDGlass – Warder Evolution** — a modern continuation of the established FullHDGlass experience.
