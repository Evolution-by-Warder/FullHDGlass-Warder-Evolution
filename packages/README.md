# FullHDGlass Warder Evolution – production IPK staging

**Schválená retenčná politika: 23. novembra 2026.** Hlavný Git obsahuje najnovšie **maximálne štyri ostré vydania**: **1.0.84, 1.0.83, 1.0.82 a 1.0.80**. Identita interného opkg balíka sa nemení: `enigma2-plugin-skins-fullhdglass-warder-evolution`.

**Dve dočasné migračné výnimky (nie sú rollback verzie):**
- `enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk` a SHA: starý `update.json` musí ešte umožniť prípravu prechodu z pôvodnej identity `enigma2-skin-fullhdglass17`.
- `enigma2-plugin-skins-fullhdglass_1.0.72_all.ipk` a SHA: historický TEST runtime v skutočne existujúcej vetve `warder-modernization-work/update-test.json` naň stále odkazuje. Do vyčistenia tejto samostatnej aktualizačnej cesty sa nesmie zmazať.

`update-production.json` a nový `main/update-test.json` smerujú na overené `1.0.84`; starý `update.json` ostáva kompatibilným bootstrapom `1.0.18` a následne smeruje na produkčný feed. Nezamieňať hlavný test feed s historickým branch TEST feedom.

Každé ďalšie stabilné vydanie publikuje nemenný IPK a SHA-256 na GitHub Releases. Produkčný publisher ponechá v `main/packages/` aktuálne a predchádzajúce tri ostré verzie, a až po overenom GitHub Release a správnom update feede odstráni iba prebytočné staré dvojice. Výnimky môže odblokovať iba osobitné overenie migrácie. Zmeny nikdy nemažú Git históriu, tagy, originálne SAT ZIPy, MASTER grafiky ani zálohy. `packages/test` je ignorovaný testovací výstup, nie produkčný archív.

Podrobnosti: `docs/RELEASE_RETENTION_POLICY.md` a `docs/ECOSYSTEM-CLEANUP-CHECKPOINT-20261123.md`.
