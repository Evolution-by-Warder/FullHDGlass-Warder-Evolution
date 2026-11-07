# PR #51 experimental source patch - not a feed release.
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append:openatv = " file://0001-progressbar-event-independent-of-epg-font.patch"
