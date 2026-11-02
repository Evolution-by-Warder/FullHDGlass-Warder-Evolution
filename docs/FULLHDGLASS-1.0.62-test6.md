# FullHDGlass 1.0.62-test6 — framed preview alignment TEST

Keep all existing frame artwork and layout coordinates. The reported photograph resembles ChannelSelection type 28 (with PIG 4); it does not establish the receiver/image or exact overscan settings. Source review shows eVideoWidget maps widget coordinates to the video plane independently of /proc/stb/fb OSD positioning. A moved or reduced OSD viewport can therefore displace the decorative frame relative to the video. This mechanism matches the symptom and still requires confirmation on the reporting receiver.

New scoped renderers project framed video through the existing 720x576 OSD viewport, using the actual framebuffer size and current parent offset. Native Position/Size are preserved, avoiding accumulated movement after repeated show/hide. Native decoder selection, PiP activation, radio-only visibility and fullscreen restoration are inherited. No hardware nodes, image controllers, global Pig class or OSD settings are written. Missing, full-size or unrecognised viewport data retain native geometry.

Applied to all 15 catalogued framed ChannelSelection templates: 2, 4, 9, 10, 11, 15, 21, 27, 28, 29, 30, 31, 32, 38, 41. Type 27 is a legacy MiniTV template not present in the standard choice list; its PiP lifecycle is retained. Artwork, nominal rectangles, frame pixmaps and radio fallback rectangles are unchanged. Other screens use their existing renderer.

Six regressions verify projection at HD/FHD/WQHD/UHD framebuffer sizes, unavailable/malformed/out-of-range/full OSD data, parent offsets, native Pig show/hide and decoder behavior, repeated opens, legacy MiniTV activation/cleanup and every framed template. Matrices use actual OpenPLi and OpenATV Pig classes. Final IPK verification repeats these tests on extracted package files.

Includes all test5 OpenPLi dialog and earlier plugin-browser repairs. Independent TEST only. Production release/promotion remains paused at the user's instruction. Physical receiver confirmation remains pending.
