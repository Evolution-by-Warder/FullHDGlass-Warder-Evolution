# Channel selection picons — 5 November 2026

**1.0.69 update:** the 50x30 behavior described below is now opt-in. The default
restores the original image lookup. See [setting and migration](CHANNEL-PICON-SOURCE-20261105.md).

When a user keeps a separate 50x30 set, the channel rows must show that set
while the selected-service preview keeps its own larger artwork. When a
particular small picon is absent, the row uses the matching shared picon.

## Resulting lookup

The base is the skin's existing Picons/Icons path, resolved to `hdg17_files`.
For example, a USB installation uses `/media/usb/hdg17_files`.

| Place | Priority | Fallback |
| --- | --- | --- |
| Channel-list row | `picon_50x30` | `picon`, then the image's existing lookup |
| Large selected-service preview | Its existing selected folder | Shared `picon` |

The row fallback applies to each service, including partly filled small sets.
An absent or empty small folder allows one shared set to serve all rows.
Small and large artwork can therefore retain different colours or styles.
Reference, alternative-group, IPTV, namespace and service-name aliases are
resolved within the small folder before moving to the shared folder.

The adapter changes the lookup imported by `Components.ServiceList` in memory
only while FullHDGlass is active. This covers the native C++ callback path and
the newer OpenATV template painter. The native image renderer, other skins,
the image's picon visibility toggle and its final fallback remain in control.
Lookups read the current configured base and do not cache missing picons.

No path is hardcoded to USB. No system files or symlinks are written and no
image setting is changed. The playing-service extra infobar, LCD/display,
provider/satellite logos, artwork and approved screen geometry are outside
this change. The existing selected-preview `g17RefTV` lookup already supports
the shared folder; `g17RefTV3` now has that fallback for large formats too.

## Validation and delivery

`tools/test-channel-picons.py` exercises real temporary paths, the shipped
lookup and large-preview function, and the native ServiceList callback/template
handoffs. Pass `--upstream PATH/lib/python` to check a supplied image source.
The test is included in the OpenATV and OpenPLi compatibility matrices.
The exact startup hook is recorded in the existing controller change ledger;
an altered hook must still fail the frozen controller fingerprint check.

The owner authorized normal FullHDGlass 1.0.68 publication on 5 November 2026
so the reported behavior can be checked on a receiver. The immutable package
and both installed update channels are verified by the release workflow.
On 5 November 2026 the reporting user confirmed that the restored behavior
matches the original request: “ano super je to ono přesně tak to bylo”.
Their earlier report identified OpenATV 8.1. The confirmation did not identify
the specific receiver or establish testing of all three reported models.
The publication-time host-test flag remains a historical record.

