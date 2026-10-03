# TEST93 Radio Layout Contract

Authoritative visual basis: approved clean Radio master, 1671x941 pixels.
Target Enigma2 canvas: 1920x1080. Scale is approximately 1.149 on both axes.

These coordinates are design anchors. Do not move active widgets independently without updating this contract and re-validating against the approved master.

- Top glass active area: x 27..1864, y 15..101.
- Date/day: x=62 y=32 w=610 h=52.
- Unified HH:MM:SS clock: x=745 y=27 w=340 h=58.
- Branding: x=1280 y=30 w=520 h=50.
- Center artwork: x=620 y=134 w=648 h=648. Artwork MUST remain square; it is centered inside the master frame rather than stretched to the non-square generated frame.
- Bottom glass active area: x 27..1864, y 813..1035.
- Service picon: x=70 y=852 w=280 h=160.
- Service name: x=420 y=842 w=720 h=42.
- RadioText: x=420 y=895 w=1000 h=52.
- RtpText: x=420 y=955 w=1000 h=38.
- Decorative spectrum: x=1470 y=838 w=350 h=126.
- Dynamic service/provider field: x=1470 y=978 w=350 h=38, centered. This is the real ServiceName/Provider output (for example ARD BR or the value supplied by another service); never bake DAB+ into the background.

Protected behavior:
- TEST92 first-entry radio overlay recovery must not change.
- WarderRadioArtwork exact-match behavior must not change.
- Native Screens.RdsDisplay.RdsInfoDisplay must not be replaced or monkey-patched.
- Native DAB SLS/passive radio fallback must remain available.
- WarderRadioSpectrum is decorative only and must not be described as audio-reactive.
