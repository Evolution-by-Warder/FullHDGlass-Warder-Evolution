#!/bin/sh
# Warder PR51 — read-only Enigma2 build provenance audit.
# No updates, no service restarts, no write operations, no credentials.
set -u
echo "=== image and exact build identifiers ==="
if [ -r /etc/image-version ]; then
    grep -E '^(box_type|version|build|date|oever|distro|imageversion|imagebuild|imagetype|arch|compile-date|compile-datetime)=' /etc/image-version || :
fi
echo "=== package metadata (no feed or install) ==="
if command -v opkg >/dev/null 2>&1; then
    opkg status enigma2 2>/dev/null | grep -E '^(Package|Version|Architecture|Source|SourceName|Maintainer|Filename|SourceDateEpoch|OE|Depends):' || :
    opkg info enigma2 2>/dev/null | grep -E '^(Package|Version|Architecture|Source|SourceName|Maintainer|Filename|SourceDateEpoch|OE):' || :
fi
echo "=== local opkg lists matching installed version ==="
if [ -r /usr/lib/opkg/status ]; then
    awk 'BEGIN { RS=""; FS="\n" } /^Package: enigma2\n/ { for (i=1;i<=NF;i++) if ($i ~ /^(Package|Version|Architecture|Source|Filename|Maintainer):/) print $i }' /usr/lib/opkg/status
fi
echo "=== available read-only build metadata candidates ==="
for file in /etc/enigma2-version /etc/enigma2-version.info /etc/build-info /etc/buildinfo /etc/oe-alliance-buildinfo /etc/oe-build-info /etc/version; do
    if [ -f "$file" ] && [ -r "$file" ]; then
        printf '%s: ' "$file"
        sed -n '1,3p' "$file" | cut -c 1-180
    fi
done
echo "=== architecture ==="
uname -m
echo "=== end: NO CHANGES MADE ==="
