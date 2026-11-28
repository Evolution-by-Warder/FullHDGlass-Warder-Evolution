#!/bin/sh
# Iba v jednorazovej kópii firmware, sieť odpojená. Reálny opkg/Python/hooky.
set -eu
test -e /skuska/izolovane
cat /etc/os-release
opkg --version
mkdir -p /etc/enigma2 /run /var/volatile/tmp /var/volatile/log
chmod 1777 /tmp
for ipk in /skuska/*.ipk; do cp "$ipk" /tmp/; done
old=/tmp/enigma2-plugin-skins-fullhdglass_1.0.94_all.ipk
bad=/tmp/enigma2-plugin-skins-fullhdglass_1.0.96_all.ipk
opkg install "$old"
printf '\nconfig.plugins.setupGlass17.warder_probe=retain-625\n' >> /etc/enigma2/settings
printf '#NAME Receiver probe\n' > /etc/enigma2/userbouquet.warder_probe.tv
printf '\n<!-- warder-probe -->\n' >> /etc/enigma2/skin_user-hdg17.xml
sha256sum /etc/enigma2/settings /etc/enigma2/userbouquet.warder_probe.tv /etc/enigma2/skin_user-hdg17.xml >/tmp/wanted
opkg install "$bad"
test -s /usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderResolution.mipsel-linux-gnu.abi3.so
sha256sum -c /tmp/wanted
sh /skuska/obnova-fullhdglass.sh
sha256sum -c /tmp/wanted
grep -qx '4' /tmp/init-events
grep -qx '3' /tmp/init-events
opkg files enigma2-plugin-skins-fullhdglass-warder-evolution | grep -q '/setupGlass17/warderResolution.py'
echo WARDER_VUZERO_OPKG_096_TO_094_PASS
