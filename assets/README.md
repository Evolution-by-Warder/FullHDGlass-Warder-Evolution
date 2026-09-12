# FullHDGlass17 legacy downloadable assets

This directory tracks the downloadable asset families used by the original FullHDGlass17 Download menu. The original plugin fetched these from `ftp.hdglass.eu`.

## Legacy download families

1. Channel picons 400x240 (`picon_400x240`)
2. Channel picons 220x132 (`picon_220x132`)
3. Provider picons 220x132 (`piconProv-220`)
4. Satellite picons 220x132 (`piconSat-220`)
5. Black channel picons (`picon`)
6. Black 50x30 channel picons (`picon_50x30`)
7. Black provider picons (`piconProv-b`)
8. Black satellite picons (`piconSat-b`)
9. Black CAM picons (`piconCam-b`)
10. Black weather picons (`piconWeather-b`)
11. White channel picons (`picon`)
12. White 50x30 channel picons (`picon_50x30`)
13. White provider picons (`piconProv-w`)
14. White satellite picons (`piconSat-w`)
15. White CAM picons (`piconCam-w`)
16. White weather picons (`piconWeather-w`)
17. OLED picons (`piconOled`)
18. ZZPicon CZ/SK (`ZZPicon-v`)
19. Help graphics (`help`)
20. Icon sets and previews (`icon_sets_preview`)
21. ExtraScreens graphics (`extraScreens`)
22. Menu icons (`menuicons`)
23. Large menu icons (`menuiconsbig`)
24. Weather icons (`weatherIconsN`)
25. Animated weather icons (`animWeatherIcons`)
26. 7zip helper binaries (`7zip-aa`, `7zip-a`, `7zip-m`, `7zip-s` depending on CPU)
27. Large ChannelSelection icons (`CHSPiconbig`)

## Legacy server status

As of 2026-09-12 the legacy host `ftp.hdglass.eu` does not resolve from the migration environment, so a direct complete mirror cannot currently be produced from the original FTP host.

Public historical references confirm that these assets were intended to be downloaded through the FullHDGlass17 Download menu and were maintained separately from the skin package.

## Warder Evolution plan

Recovered asset archives will be stored under this tree and indexed by a machine-readable manifest. FullHDGlass17 Warder Evolution will use HTTPS/GitHub instead of embedded FTP credentials.

No legacy FTP credentials will be retained in the Warder Evolution codebase.
