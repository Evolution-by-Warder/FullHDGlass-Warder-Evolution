# TEST261 small settings assets

Built-in imagegen mode from the imagegen skill was used for the 19 download-icon background extractions and the plugin icon. No external API/CLI image model was used. The original skin PNGs are retained byte-for-byte. The generated project assets live under `source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/images/`; their exact hashes and dimensions are in `settings-batch261-assets.json`. Large generation originals are not packaged.

Download edit prompt (each source icon separately):

> Use case: background-extraction. Production menu PNG edit. Remove ONLY the flat black backdrop (outside AND inside the frame behind the object) from this exact icon. Preserve the original foreground object, all text exactly, any metallic dark details, blue rectangular frame/glow if present, original colors, proportions and composition. Do not erase dark foreground objects; remove only background. Genuine alpha transparency, no checkerboard or replacement backdrop. No redesign, no additions. Match the source landscape aspect ratio (189:123), or square for the red X / green arrow. Small UI icon used at 116x74 pixels. For a red X / green down-arrow preserve its exact shape and color.

Satellite dish variant: remove only the black background including the flat black interior behind the dish; preserve dish, metallic pedestal, glowing blue rectangular frame, proportions and foreground detail. Actual alpha transparency, no added elements or text.

Plugin icon prompt:

> Use case: logo-brand. Supporting style reference: supplied approved FullHDGlass by Warder banner. Create a compact Enigma2 plugin-list icon for its settings/configuration entry, landscape 4:3 composition. Preserve the recognizable chrome cybernetic skull with red eyes and blue/cyan glowing details, make it smaller on the LEFT. Beside it put large crisp readable text exactly 'FullHDGlass' with 'by Warder' smaller beneath. A small cyan gear can indicate configuration. Rich dark navy background matching reference. Fill the icon area with readable logo, restrained blue glow, professional compact UI asset, no date, no time, no extra slogans, no PiconHub text.

The owner additionally requested image compression. Packaging normalization uses maximum 189×123 for category icons, 50×50 for the status symbols and 160×120 for the plugin icon, retaining generated alpha and aspect ratios. Original full-size skin assets are not resampled. Build-time lossless PNG optimization replaces IDAT only and checks exact RGBA equality plus unchanged non-IDAT chunks.

78 real type thumbnails are derived deterministically by `tools/build-type-previews.py` from the pinned stock `more_icons.zip` (SHA256 0fca8510b5e1e7dd600548f706553b83a3993e91077382aba4c6363278eac230). They are 174×98 with an opaque navy backing; no large screenshot decoding happens while constructing the type list.
