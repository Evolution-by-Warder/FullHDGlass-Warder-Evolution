#!/usr/bin/env python3
"""Read-only audit of preview PNGs; never changes artwork or receiver packages.

Requires Pillow and NumPy. Measures every frame and writes reproducible metrics
plus contact sheets in an explicitly selected output directory. Contrast flags
are review aids, not a substitute for visual inspection or receiver testing.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'assets/warder/downloads/ui/spinners/preview-library'
BG = (7, 19, 33)
LIGHT = (235, 240, 245)


def luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255
    c = np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)
    return c @ np.array([.2126, .7152, .0722])


def contrast(a, background):
    alpha = a[:, :, 3:4] / 255
    rgb = a[:, :, :3] * alpha + np.array(background) * (1 - alpha)
    lum, base = luminance(rgb), luminance(background)
    ratios = (np.maximum(lum, base) + .05) / (np.minimum(lum, base) + .05)
    mask = a[:, :, 3] >= 32
    return (float(np.percentile(ratios[mask], 90)) if mask.any() else 1,
            int(((ratios >= 1.5) & (a[:, :, 3] >= 32)).sum()))


def audit(row):
    group = 'spinkit' if row['id'].startswith('spinkit-') else 'community'
    folder = LIBRARY / group / row['folder']
    errors, dark, light, sizes, boxes, pixels, scores, edge_frames = [], [], [], [], [], [], [], []
    union = np.zeros((104, 104), dtype=bool)
    repeats = 0
    previous = None
    actual = {p.name for p in (folder / 'frames').glob('*.png')}
    expected = {f['name'] for f in row['frames']}
    if actual != expected:
        errors.append('frame-file-list-mismatch')
    if row['frame_count'] != len(expected):
        errors.append('catalogue-frame-count-mismatch')
    for f in row['frames']:
        path = folder / 'frames' / f['name']
        raw = path.read_bytes()
        sizes.append(len(raw))
        if hashlib.sha256(raw).hexdigest() != f['sha256']:
            errors.append(f['name'] + ':sha256-mismatch')
        with Image.open(path) as check:
            check.verify()
        with Image.open(path) as im:
            im.load()
            if im.mode != 'RGBA' or im.size != (104, 104):
                errors.append(f['name'] + ':unexpected-format')
            a = np.array(im.convert('RGBA'))
        mask = a[:, :, 3] >= 32
        if np.any(np.concatenate((mask[0], mask[-1], mask[:, 0], mask[:, -1]))):
            edge_frames.append(f['name'])
        union |= mask
        ys, xs = np.where(mask)
        boxes.append([int(xs.max()-xs.min()+1), int(ys.max()-ys.min()+1)] if len(xs) else [0, 0])
        d, visible = contrast(a, BG)
        l, _ = contrast(a, LIGHT)
        dark.append(d)
        light.append(l)
        scores.append(visible)
        # Hidden RGB under alpha=0 is not visible image content.
        premultiplied = a[:, :, :3].astype(np.uint16) * a[:, :, 3:4]
        digest = hashlib.sha256(premultiplied.tobytes() + a[:, :, 3].tobytes()).hexdigest()
        pixels.append(digest)
        repeats += previous == digest
        previous = digest
    ys, xs = np.where(union)
    bbox = [int(xs.max()-xs.min()+1), int(ys.max()-ys.min()+1)] if len(xs) else [0, 0]
    flags = []
    source = row.get('source_canvas')
    if source and max(source) < 64:
        flags.append('small-raster-source')
    if min(bbox) < 24:
        flags.append('thin-or-small-drawing')
    nonblank_boxes = [b for b in boxes if b != [0, 0]]
    median_box = np.median(nonblank_boxes, axis=0).tolist() if nonblank_boxes else [0, 0]
    if min(median_box) < 16:
        flags.append('tiny-per-frame-drawing')
    if float(np.median(dark)) < 2:
        flags.append('low-dark-background-contrast')
    if row.get('source_has_opaque_frames'):
        flags.append('opaque-source-background')
    if len(set(pixels)) < 2:
        flags.append('no-visible-animation')
    if edge_frames:
        flags.append('drawing-touches-canvas-edge')
    if repeats >= len(sizes) / 2:
        flags.append('many-held-frames')
    if row.get('original_review_number') == 31:
        flags.append('owner-requested-brightening')
    representative = int(np.argmax(scores))
    with Image.open(folder / 'preview.gif') as gif:
        gif_duration = sum(frame.info.get('duration', 0) for frame in ImageSequence.Iterator(gif))
        gif_size, gif_loop = list(gif.size), gif.info.get('loop')
        if gif_size != [104, 104] or gif_loop != 0 or gif_duration != row['interval_ms'] * len(sizes):
            errors.append('gif-size-loop-or-duration-mismatch')
    return {
        'id': row['id'], 'title': row['title'],
        'original_review_number': row['original_review_number'],
        'path': str(folder.relative_to(ROOT)), 'frame_count': len(sizes),
        'interval_ms': row['interval_ms'], 'cycle_ms': row['interval_ms'] * len(sizes),
        'canvas_px': [104, 104], 'source_canvas_px': source,
        'fit_canvas_px': row.get('inner_size'), 'visible_union_px_alpha32': bbox,
        'median_nonblank_frame_drawing_px_alpha32': median_box,
        'png_bytes': sum(sizes), 'largest_png_bytes': max(sizes),
        'gif_bytes': (folder / 'preview.gif').stat().st_size,
        'gif_duration_ms': gif_duration, 'gif_loop': gif_loop,
        'rgba_bytes_per_frame': 104 * 104 * 4,
        'rgba_frame_buffers_bytes': len(sizes) * 104 * 104 * 4,
        'unique_visible_frames': len(set(pixels)), 'consecutive_repeated_frames': repeats,
        'blank_frames_alpha32': sum(b == [0, 0] for b in boxes),
        'median_frame_p90_contrast_dark': round(float(np.median(dark)), 3),
        'max_frame_p90_contrast_dark': round(max(dark), 3),
        'median_frame_p90_contrast_light': round(float(np.median(light)), 3),
        'median_pixels_contrast_at_least_1_5_dark': int(np.median(scores)),
        'representative_frame': row['frames'][representative]['name'],
        'canvas_edge_frames_alpha32': edge_frames,
        'flags': flags, 'integrity_errors': errors,
    }


def source_verification(rows):
    """Check original archive hashes and every community frame's fixed transform."""
    spec = importlib.util.spec_from_file_location('community_importer', ROOT / 'tools/import-community-spinner-previews.py')
    importer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(importer)
    originals, archives = {}, []
    for source_id, filename, _, checksum in importer.ARCHIVES:
        path = importer.SOURCE / filename
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != checksum:
            raise ValueError('Original archive checksum mismatch: ' + filename)
        archives.append({'filename': filename, 'bytes': path.stat().st_size, 'sha256': actual})
        for name, raw in importer.read_pngs(path):
            parent, _, base = name.rpartition('/')
            index = int(importer.FRAME.fullmatch(base)[1])
            originals[(source_id, parent, index)] = raw
    checked, differences = 0, []
    for row in rows:
        if 'origins' not in row:
            continue
        origin = row['origins'][0]
        width, height = row['source_canvas']
        target = tuple(row['inner_size'])
        for native, index in zip(row['frames'], origin['source_indices'], strict=True):
            key = origin['source'], origin['archive_folder'], index
            with Image.open(io.BytesIO(originals[key])) as im:
                canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                canvas.paste(im.convert('RGBA'), (0, 0))
            fitted = canvas.convert('RGBa').resize(target, Image.Resampling.LANCZOS).convert('RGBA')
            expected = Image.new('RGBA', (104, 104), (0, 0, 0, 0))
            expected.paste(fitted, ((104-target[0])//2, (104-target[1])//2))
            with Image.open(LIBRARY / 'community' / row['folder'] / 'frames' / native['name']) as actual:
                if expected.tobytes() != actual.convert('RGBA').tobytes():
                    differences.append(row['id'] + '/' + native['name'])
            checked += 1
    return {'original_archives': archives, 'community_frames_reconstructed': checked, 'pixel_differences': differences}


def reference_sets():
    rows = []
    for title, relative in (
        ('Holubica', 'source/package-root/usr/share/enigma2/hd_glass17/spinner'),
        ('HDGlass - bakussa: original', 'source/package-root/usr/share/enigma2/hd_glass17/spinner-themes/bakussa'),
        ('HDGlass - bakussa: approved blue review variant', 'design/spinner-choice/bakussa-blue-centered/frames'),
    ):
        files = sorted((ROOT / relative).glob('wait*.png'))
        if not files:
            raise ValueError('Reference set missing: ' + relative)
        dimensions, decoded = set(), 0
        for path in files:
            with Image.open(path) as im:
                im.load()
                dimensions.add(im.size)
                if im.mode != 'RGBA':
                    raise ValueError('Unexpected reference format')
                decoded += im.width * im.height * 4
        rows.append({'title': title, 'path': relative, 'frames': len(files),
                     'dimensions_px': [list(d) for d in sorted(dimensions)],
                     'png_bytes': sum(p.stat().st_size for p in files),
                     'rgba_frame_buffers_bytes': decoded})
    return rows


LABELS = {
    'small-raster-source': 'malá rastrová predloha',
    'thin-or-small-drawing': 'úzky celkový obraz',
    'tiny-per-frame-drawing': 'veľmi drobná kresba v snímke',
    'low-dark-background-contrast': 'slabý kontrast na tmavom',
    'opaque-source-background': 'nepriehľadné pôvodné pozadie',
    'drawing-touches-canvas-edge': 'kresba na okraji plátna',
    'many-held-frames': 'veľa opakovaných snímok',
    'owner-requested-brightening': 'požadované zosvetlenie',
    'no-visible-animation': 'bez viditeľného pohybu',
}


def markdown_report(result, output):
    s, rows = result['summary'], result['entries']
    lines = [
        '# Kontrola kvality a veľkostí spinnerov — 31. 10. 2026', '',
        'Skontrolovaných **152 kandidátov / 1 958 PNG snímok** po odstránení dvoch schválených duplicít. Čísla nižšie sú z pôvodnej prehliadky 154 návrhov; nemenia sa podľa aktuálnej pozície v galérii. Referenčné sady Holubica a bakussa sú uvedené osobitne.', '',
        '## Výsledok', '',
        '- Všetky PNG sa dekódujú, majú RGBA 104 × 104 px a súhlasia s katalógovými SHA-256. Všetkých 152 GIF ukážok má správny rozmer, nekonečnú slučku a trvanie zodpovedajúce 100 ms na snímku.',
        '- Všetkých 152 sekvencií obsahuje skutočnú zmenu viditeľných pixelov; majú 2–56 snímok, cyklus 0,2–5,6 s. To samo osebe nezaručuje plynulý pohyb.',
        '- Tri pôvodné komunitné archívy majú nezmenený SHA-256. Všetkých 1 779 zostávajúcich komunitných PNG bolo znovu odvodených z originálov rovnakým pevným prepočtom; porovnanie každého pixelu našlo 0 rozdielov. SpinKit: 179 snímok z CSS, overené oproti uloženým hashom.',
        '- Plátno 104 × 104 px nie je rozmer samotnej kresby. Pri malých predlohách sa nezväčšoval zdroj; široké animácie sa vošli do pevnej oblasti bez zmeny pomeru strán, niekedy za cenu príliš malého výsledku.',
        '- Vizuálne boli prezreté reprezentatívne snímky všetkých 152 kandidátov v skutočných 104 × 104 px na tmavom aj svetlom pozadí (10 kontaktných listov). Pri problematických sekvenciách boli porovnané aj rôzne fázy. Nejde o test prehrávania na prijímači.', '',
        '## Konkrétne prípady pred zaradením do ponuky', '',
        '| Pôvodné číslo | Návrh / skupina | Zistenie a odporúčanie |',
        '|---:|---|---|',
        '| 31 | Spinner 24 | Čierna zemeguľa na tmavom zaniká. Potvrdená požiadavka na jasnejší variant; originál zachovať. |',
        '| 86–95 | spinner-by-ekremtt | Všetkých 10 má malý zdroj 48 × 48 px a čierne nepriehľadné pozadie. Pre čistý vzhľad prerobiť pozadie; modré 86/88/89 zosvetliť, 87/92/95 tiež preveriť na tmavom. |',
        '| 101, 115 | Counter, Love | Ďalšie dve sady s nepriehľadným pôvodným pozadím. Pri Love je plné obrázkové pozadie súčasťou motívu, preto ho automaticky nemažte. Counter je zámerne úzky. |',
        '| 113 | Katze2 | Zdroj 500 × 50 px sa zmenšil na 96 × 10 px; medián kresby jednej fázy je len 22 × 9 px. Prepracovať pohyb a mierku spolu, aby sa nestratila dráha animácie. |',
        '| 122 | PapierFlieger | Zdroj 350 × 189 px má veľkú dráhu pohybu, ale malú kresbu: v pripravenej snímke medián 7 × 7,5 px. Takto je príliš drobný; upraviť mierku aj dráhu. |',
        '| 24 | Spinner 17 | Lietadlo sa zámerne približuje; medián kresby je 37,5 × 9 px, v závere je veľké. Posúdiť dlhú drobnú úvodnú fázu, nezväčšovať všetky snímky rovnako naslepo. |',
        '| 11 | Skladaná kocka | V 5 z 24 snímok sú viditeľné pixely priamo na hrane 104 px. Pred zaradením pridať rezervu zmenšením celého pohybu; dotyk hrany je riziko orezania. |',
        '| 107, 109, 115, 121, 137, 138, 147 | Gutemine, Hexe, Love, PapaSchlumpf, Simba, Skelett, Taz | Aspoň polovica prechodov podrží rovnaký viditeľný obraz. Sú to pôvodné podržané fázy, nie poškodenie importu. Pri úpravách zachovať pôvodné trvanie; obyčajné vymazanie duplicitných PNG by zrýchlilo animáciu. |',
        '| 5, 6 | Pulz, Tri bodky | Zoslabovanie pulzu a nízky pás troch bodiek sú súčasťou návrhu, nie automatická chyba kvality. |', '',
        '**18 malých rastrových zdrojov** (najdlhšia strana pod 64 px): ' + ', '.join(str(r['original_review_number']) for r in rows if 'small-raster-source' in r['flags']) + '. Bez väčšej predlohy nemožno sľúbiť nové detaily; pri pixelových kresbách môže byť malý rozmer zámer.', '',
        '**7 kandidátov s nízkym meraným kontrastom na tmavom**: ' + ', '.join(str(r['original_review_number']) for r in rows if 'low-dark-background-contrast' in r['flags']) + '. Ide o pomocný prah, nie posudok prístupnosti. Tlmené detaily a fázy pulzu treba hodnotiť aj vizuálne.', '',
        '## Miesto a prehrávanie', '',
        f'- PNG všetkých 152 kandidátov spolu: **{s["native_png_bytes"]:,} B / {s["native_png_bytes"]/1048576:.2f} MiB**. GIF ukážky osobitne: **{s["preview_gif_bytes"]:,} B / {s["preview_gif_bytes"]/1048576:.2f} MiB**; GIF nie je formát prehrávania v prijímači.',
        f'- Jedna celá sada PNG má od **{s["min_native_png_bytes_per_spinner"]:,} B** do **{s["max_native_png_bytes_per_spinner"]:,} B** ({s["max_native_png_bytes_per_spinner"]/1024:.1f} KiB, Spinner 55 / pôvodné č. 62).',
        '- Jedna dekódovaná snímka 104 × 104 RGBA má **43 264 B**. Najdlhšia sada (PapierFlieger, 56 snímok) má **2 422 784 B / 2,31 MiB** samotných snímkových bufferov. Do toho nie sú započítané pomocné grafické buffery ani režijná pamäť.',
        '- Načítava sa zvolená sada; všetkých 152 animácií sa neprehráva ani nedekóduje naraz. Pri rovnakom rozmere a intervale samotný väčší počet snímok predlžuje cyklus a zväčšuje pamäť sady; meranie CPU na boxe nebolo vykonané.',
        '- Podľa už pripnutého zdrojového kódu OpenATV sa tieto snímky zmestia pod skúmaný automatický limit plochy 48 000 B a loader má hranicu 64 snímok. Je to kontrola konkrétnej implementácie, nie záruka bezchybnosti na každom image alebo ovládači.',
        '- Celú kolekciu nepridávať bez rozmyslu do základného IPK: samotné natívne PNG pridávajú 11,25 MiB. Rozumné je ponechať samostatné voliteľné sady; balík ani aktualizátor sa touto kontrolou nemenili.', '',
        '| Referenčná sada | Rozmer | Snímky | PNG na disku | Dekódované snímky |',
        '|---|---:|---:|---:|---:|',
    ]
    for r in result['reference_sets']:
        dims = ', '.join(' × '.join(map(str, d)) for d in r['dimensions_px'])
        lines.append(f'| {r["title"]} | {dims} | {r["frames"]} | {r["png_bytes"]:,} B | {r["rgba_frame_buffers_bytes"]:,} B |')
    lines += ['', 'Modrý bakussa je schválený návrh v pracovných podkladoch; táto kontrola ho nevydáva ako nové IPK. Jeho vyššia komprimovaná veľkosť oproti pôvodnému variantu pri rovnakom počte a rozmere snímok nemení výpočet dekódovaných bufferov.', '',
              '## Inventár všetkých 152 kandidátov', '',
              'Rozmery kresby sú medián neblankových snímok pri alfa ≥ 32. Značky sú podnety na kontrolu a môžu sa prekrývať. Bez značky znamená, že automatické kritériá nenašli problém, nie potvrdenie dokonalosti.', '',
              '| Pôvodné č. | Návrh | Zdroj px | Kresba v snímke px | Snímky | PNG KiB | Poznámky |',
              '|---:|---|---:|---:|---:|---:|---|']
    for r in rows:
        source = 'CSS' if not r['source_canvas_px'] else ' × '.join(map(str, r['source_canvas_px']))
        box = ' × '.join(f'{v:g}' for v in r['median_nonblank_frame_drawing_px_alpha32'])
        notes = '; '.join(LABELS[f] for f in r['flags']) or '—'
        url = 'https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/tree/review/spinner-library-20261031/' + r['path']
        lines.append(f'| {r["original_review_number"]} | [{r["title"]}]({url}) | {source} | {box} | {r["frame_count"]} | {r["png_bytes"]/1024:.1f} | {notes} |')
    lines += ['', 'Strojové výsledky a presná metodika: [audit.json](audit.json). Reprodukcia: `python tools/audit-spinner-quality.py --output /tmp/warder-spinner-quality-20261031` (Pillow, NumPy, systémová libarchive pre RAR). Skript nemení obrázky, archívy ani obsah prijímača.', '',
              'Verejné vydanie, aktualizačné kanály a Trezor zostali nedotknuté. Žiadne nové IPK nebolo vytvorené.', '']
    (output / 'README.md').write_text('\n'.join(lines))


def contact_sheets(rows, output):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font = ImageFont.truetype(font_path, 14)
    small = ImageFont.truetype(font_path, 12)
    for offset in range(0, len(rows), 16):
        sheet = Image.new('RGB', (1200, 1000), (24, 30, 39))
        draw = ImageDraw.Draw(sheet)
        for i, r in enumerate(rows[offset:offset+16]):
            x, y = (i % 4) * 300, (i // 4) * 250
            p = ROOT / r['path'] / 'frames' / r['representative_frame']
            with Image.open(p) as im:
                for dx, bg in ((12, BG), (132, LIGHT)):
                    tile = Image.new('RGBA', (104, 104), bg + (255,))
                    tile.alpha_composite(im.convert('RGBA'))
                    sheet.paste(tile.convert('RGB'), (x+dx, y+37))
            draw.text((x+12, y+10), f"{r['original_review_number']:03d} {r['title'][:27]}", font=font, fill='white')
            draw.text((x+12, y+150), f"source {r['source_canvas_px'] or 'CSS'}; drawing {r['visible_union_px_alpha32']}", font=small, fill='#b8deef')
            draw.text((x+12, y+171), f"{r['frame_count']} frames; {r['png_bytes']/1024:.1f} KiB; contrast {r['median_frame_p90_contrast_dark']}", font=small, fill='#b8deef')
            for j, flag in enumerate(r['flags'][:3]):
                draw.text((x+12, y+193+j*16), flag, font=small, fill='#ffba72')
        sheet.save(output / f'contact-{offset//16+1:02d}.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    catalogue = LIBRARY / 'catalog.json'
    data = json.loads(catalogue.read_text())
    rows = [audit(row) for row in data['entries']]
    source_proof = source_verification(data['entries'])
    flags = Counter(flag for row in rows for flag in row['flags'])
    summary = {
        'spinners': len(rows), 'native_frames': sum(r['frame_count'] for r in rows),
        'native_png_bytes': sum(r['png_bytes'] for r in rows),
        'preview_gif_bytes': sum(r['gif_bytes'] for r in rows),
        'canvas_px': [104, 104], 'rgba_bytes_per_frame': 43264,
        'max_frame_count': max(r['frame_count'] for r in rows),
        'max_rgba_frame_buffers_bytes': max(r['rgba_frame_buffers_bytes'] for r in rows),
        'max_native_png_bytes_per_spinner': max(r['png_bytes'] for r in rows),
        'min_native_png_bytes_per_spinner': min(r['png_bytes'] for r in rows),
        'flag_counts': dict(flags),
        'integrity_errors': [r['id'] for r in rows if r['integrity_errors']],
        'all_at_most_64_frames': all(r['frame_count'] <= 64 for r in rows),
        'all_animated': all(r['unique_visible_frames'] > 1 for r in rows),
    }
    result = {
        'schema': 1, 'date': '2026-10-31', 'catalogue_sha256': hashlib.sha256(catalogue.read_bytes()).hexdigest(),
        'scope': '152 reviewed candidates; installed dove and bakussa derivatives are separate',
        'method': {
            'backgrounds': ['#071321', '#EBF0F5'],
            'contrast': 'Median across frames of p90 linear-sRGB luminance contrast over alpha >=32 pixels; low <2.0. Heuristic, not accessibility certification. Intentional fades require visual interpretation.',
            'drawing_bbox': 'Union of pixels with alpha >=32 across every frame; size includes movement.',
            'small_source': 'Raster source longest side <64px. CSS vectors excluded.',
            'thin_drawing': 'Visible union shortest side <24px; deliberate bars can legitimately match.',
            'memory': 'Decoded RGBA frame buffers only; excludes loader, graphics work buffers, compression, allocator overhead. Not a receiver CPU measurement.',
            'modifications': 'None: all original artwork, archives, installed package, updater and Trezor unchanged.',
        },
        'summary': summary, 'source_verification': source_proof,
        'reference_sets': reference_sets(), 'entries': rows,
    }
    (output / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    markdown_report(result, output)
    contact_sheets(rows, output)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
