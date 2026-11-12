# FullHDGlass – Warder Evolution 1.0.80

Stable update integrating the combined visual and control fixes prepared on 12 November 2026.

## Channel selection and remote control
- Restored a full-screen classic channel list layout (type 12) for OpenATV 7.6, including cleaner text sizing and spacing.
- In Warder Neutrino mode on OpenATV 7.6, a short OK press opens the channel list; long OK continues to work. The system `keymap.ntr` is not changed.

## EPG and media lists
- Reworked the Full HD Vertical Program Guide and Vertical Program Guide PiG layouts with smaller, better-aligned elements.
- Restored the original dark semi-transparent backdrop (`#50000000`) in both Vertical EPG variants without losing their full-screen 1920×1080 layout.
- Improved list and text/progress spacing for Enhanced Movie Center (EMC), Single EPG and EPG Search to reduce overlap and truncation.
- Aligned the four colored key labels and added a date-format example in the settings.

## Spinner selection
- Bakussa is the new Warder default spinner.
- The receiver image's native spinner remains available as the first, system-language-labeled option in the spinner selector.
- Existing user spinner preferences and other remote-control modes remain supported.

## Compatibility and verification
- Automated integration and complete IPK packaging checks for the OpenATV 7.6 candidate passed before release.
- The release pipeline also validates package integrity, version consistency, migration, uninstall safeguards and regression tests.
- OpenPLi and newer OpenATV images retain their respective compatibility paths; confirm the on-receiver appearance after upgrading.

The update is intended to preserve user configuration and downloaded assets. Restart the Enigma2 GUI after installing. Back up personal settings before removing the package.
