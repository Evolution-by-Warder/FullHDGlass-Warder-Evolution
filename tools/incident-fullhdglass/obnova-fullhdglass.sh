#!/bin/sh
# Núdzová obnova VU+ Zero na OpenPLi 9.2. Vyžaduje bežný shell správcu.
set -eu
umask 077
pkg=enigma2-plugin-skins-fullhdglass-warder-evolution
name=enigma2-plugin-skins-fullhdglass_1.0.94_all.ipk
digest=9dd3300cafffcdaa522b308c22dda863b6bc47ee190ba3f6c24ba235bbcd6028
url=https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v1.0.94/$name
src=/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17
fail() { echo "$*" >&2; exit 1; }
[ "$(id -u)" = 0 ] || fail "Obnova potrebuje konto root."
[ "$(uname -m)" = mips ] || [ "$(uname -m)" = mipsel ] || fail "Tento súbor je určený pre pôvodný VU+ Zero."
[ -r /proc/stb/info/vumodel ] && model=$(cat /proc/stb/info/vumodel) || model=$(cat /proc/stb/info/model)
case "$model" in zero|vuzero) ;; *) fail "Iný model prijímača."; esac
[ -r /etc/os-release ] && grep -Eiq '^ID="?openpli"?$' /etc/os-release || fail "Nesúhlasí image OpenPLi."
grep -Eq '^VERSION_ID="?9\.2(\.[0-9]+)?"?$' /etc/os-release || fail "Nesúhlasí verzia OpenPLi 9.2."
installed() {
    opkg status "$pkg" | awk -v pkg="$pkg" -v version="$1" '
        BEGIN {RS=""; FS="\n"}
        {p="";v="";s="";for(i=1;i<=NF;i++){if($i~/^Package: /)p=substr($i,10);if($i~/^Version: /)v=substr($i,10);if($i~/^Status: /)s=$i}
        if(p==pkg && v==version && s~/ ok installed$/) n++}
        END {exit n!=1}'
}
if installed 1.0.94-1; then echo 'FullHDGlass 1.0.94 je už nainštalovaný.'; exit 0; fi
installed 1.0.96-1 || fail "OPKG nepotvrdil nainštalovanú verziu 1.0.96-1."
help=$(opkg --help 2>&1 || :)
case "$help" in *--force-downgrade*) downgrade=--force-downgrade ;; *-force-downgrade*) downgrade=-force-downgrade ;; *) fail "OPKG nepodporuje riadený návrat verzie." ;; esac
[ -f /etc/enigma2/settings ] && [ ! -L /etc/enigma2/settings ] || fail "Neočakávaná cesta nastavení."
[ -f "$src/warderResolution.mipsel-linux-gnu.abi3.so" ] || fail "Neúplná inštalácia 1.0.96. Pred zásahom treba skontrolovať stav."
tmp=$(mktemp -d /tmp/warder-obnova.XXXXXX)
trap 'rm -f "$tmp/$name"; rmdir "$tmp" 2>/dev/null || :' EXIT
if [ -r "/tmp/$name" ]; then cp "/tmp/$name" "$tmp/$name"
elif command -v curl >/dev/null 2>&1; then curl -fLsS --retry 2 --connect-timeout 15 --max-time 300 -o "$tmp/$name" "$url"
else wget -O "$tmp/$name" "$url"; fi
(cd "$tmp" && printf '%s  %s\n' "$digest" "$name" | sha256sum -c -) || fail "Nesprávny SHA-256. OPKG sa nespustil."
# Pred prvou zmenou overiť miesto pre súkromnú kópiu nastavení a pracovný priestor OPKG.
free_kib=$(df -Pk /etc/enigma2 | awk 'END{print $4}')
need_kib=$(du -sk /etc/enigma2 | awk '{print $1}')
[ "$free_kib" -ge $((need_kib + 32768)) ] || fail "Na flash nie je rezerva pre bezpečnú transakciu."
init 4
n=0
while pidof enigma2 >/dev/null 2>&1; do
    n=$((n+1)); [ "$n" -le 30 ] || fail "GUI sa nezastavilo."; sleep 1
done
backup=$(mktemp -d /etc/warder-obnova.XXXXXX)
cp -a /etc/enigma2 "$backup/enigma2"
echo "Uložené nastavenia: $backup/enigma2"
# Predošlé postinst môže obnoviť vlastnú historickú zálohu; pôvodné nastavenia majú prednosť.
restore() {
    python3 - "$backup/enigma2" <<'PY'
import filecmp,os,shutil,stat,sys,tempfile
from pathlib import Path
source=Path(sys.argv[1]); dest=Path('/etc/enigma2')
for root,dirs,files in os.walk(source,followlinks=False):
    for name in dirs+files:
        src=Path(root)/name
        rel=src.relative_to(source)
        dst=dest/rel
        if dst.parent.resolve()!=dst.parent: raise SystemExit('Zmenená cesta v /etc/enigma2')
        if src.is_symlink():
            if not dst.is_symlink() or os.readlink(dst)!=os.readlink(src): raise SystemExit('Zmenený odkaz v /etc/enigma2')
        elif src.is_dir():
            if dst.is_symlink(): raise SystemExit('Zmenený adresár v /etc/enigma2')
            dst.mkdir(exist_ok=True)
        elif src.is_file():
            if dst.is_symlink() or (dst.exists() and not dst.is_file()): raise SystemExit('Zmenený typ nastavenia')
            if not dst.is_file() or not filecmp.cmp(src,dst,shallow=False):
                fd,tmp=tempfile.mkstemp(dir=dst.parent);os.close(fd)
                try:
                    shutil.copy2(src,tmp);s=src.stat();os.chown(tmp,s.st_uid,s.st_gid);os.replace(tmp,dst)
                finally:
                    if os.path.exists(tmp): os.unlink(tmp)
PY
}
rc=0
opkg "$downgrade" install "$tmp/$name" </dev/null || rc=$?
restore || fail "Obnova nastavení vyžaduje kontrolu. GUI je zastavené. Kópia: $backup"
[ "$rc" = 0 ] && installed 1.0.94-1 || fail "OPKG nedokončil návrat. GUI je zastavené. Kópia: $backup"
printf '%s  %s\n' fa121a535f0fb7a4f0009e8aa3a506e7fd679fa8ba2404da0c040b546dacc761 "$src/warderResolution.py" | sha256sum -c -
[ ! -e "$src/warderResolution.mipsel-linux-gnu.abi3.so" ] || fail "Starý natívny modul zostal na disku."
sync
init 3
echo "OPKG potvrdil FullHDGlass 1.0.94. Spúšťam GUI."
