# Approved FullHDGlass settings banner

Built-in image_gen edit mode; no CLI/API fallback. Owner approved the compact graphic on 2026-10-24. Sources were the PiconHub receiver screenshot 2(20261024-044559).jpg and its earlier generated header variants. Only the new FullHDGlass settings background is consumed; PiconHub remains unchanged.

Project asset: source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/images/warder-settings-background.png

Original generated output: generated_images/exec-b367732e-2210-43a7-9a7f-86c9c60268d9.png (copied unmodified). Native XML scales the complete background to 1920×1080. The graphic band ends around 160 display pixels, inside the 164 px header. Dynamic date/time/version are separate native widgets.

Exact final edit prompt:

> Make this SAME header MUCH SMALLER vertically. Keep the exact same complete 1672x941 canvas. The final cyan separator must be at y=110 pixels from the top, NOT y=170. The skull emblem must be only 86 pixels tall, at x=30 y=10. The main 'FullHDGlass' title should begin at x=150 y=12, about 42 pixels tall, and the 'by Warder' signature fit below within y=62..102. Main title ends before x=720. Preserve exact spelling and the same chrome/cyan style, but scale the skull down uniformly; no distortion. Keep the right blue earth horizon confined near y=88..109. Everything below y=113 is unbroken flat navy #071627. Upper-right x=850..1660 y=0..86 is dark clear negative space with absolutely no lettering or UI. No other words, no date, no time, no version, no menu. Critical: 110-pixel-tall strip across the TOP of the existing canvas, NOT 170 pixels. Leave most of the canvas as plain navy. This is a compact software banner; its very small skull and shallow height are essential.

The actual approved generated artwork, not the requested pixel boundary in the prompt, determines the 164px display region. The bitmap is pinned in settings-header-asset.json. Original radio artwork and XML retain their existing baseline digest.
