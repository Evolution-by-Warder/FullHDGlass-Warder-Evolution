"""Readable version blocks, measured with the receiver's actual list fonts."""
from pathlib import Path
import re

HEADING = re.compile(r'^(?:(?:Full\s*HD\s*Glass(?:17)?)(?:\s+Warder\s+Evolution)?\s+|(?:Version|Verzia|Verze)\s*:?\s*)?(v?\d+\.\d+(?:\.\d+)?(?:-test\d+)?)(?=$|[\s:—–-])', re.I)
DATE = re.compile(r'^\d{1,2}[./]\s*\d{1,2}[./]\s*\d{4}')


def entries(text):
    result = []
    current = {'heading': '', 'paragraphs': []}
    for original in text.splitlines():
        line = original.strip()
        if not line:
            continue
        match = HEADING.match(line)
        if match:
            if current['heading'] or current['paragraphs']:
                result.append(current)
            version = match.group(1).lstrip('vV')
            suffix = line[match.end():].strip()
            current = {'heading': 'FullHDGlass ' + version, 'paragraphs': []}
            remainder = suffix.lstrip(':—–- ').strip()
            if DATE.match(remainder) or re.match(r'^\d{1,2}\.\s+\D+\d{4}', remainder):
                current['heading'] += ' — ' + remainder
            elif remainder:
                current['paragraphs'].append(remainder)
        else:
            current['paragraphs'].append(line)
    if current['heading'] or current['paragraphs']:
        result.append(current)
    return result


def wrap(text, measure, width):
    """Fit full words; split oversized tokens without losing any characters."""
    result = []
    line = ''
    for word in text.split():
        candidate = (line + ' ' + word).lstrip()
        if measure(candidate) <= width:
            line = candidate
            continue
        if line:
            result.append(line)
            line = ''
        while word and measure(word) > width:
            lo, hi = 1, len(word)
            while lo < hi:
                middle = (lo + hi + 1) // 2
                if measure(word[:middle]) <= width:
                    lo = middle
                else:
                    hi = middle - 1
            result.append(word[:lo])
            word = word[lo:]
        line = word
    if line:
        result.append(line)
    return result


def layout(text, measure, width):
    rows = []
    for entry in entries(text)[:5]:
        if rows:
            rows.append(('rule', ''))
        if entry['heading']:
            rows.extend(('heading', value) for value in wrap(entry['heading'], lambda value: measure(value, True), width))
        body = []
        for paragraph in entry['paragraphs']:
            body.extend(wrap(paragraph, lambda value: measure(value, False), width))
        if len(body) > 2:
            last = body[1]
            while last and measure(last + '…', False) > width:
                last = last.rsplit(' ', 1)[0] if ' ' in last else last[:-1]
            body[1] = last.rstrip(' .') + '…'
        rows.extend(('body', value) for value in body[:2])
    return rows


def populate(screen, filename):
    from enigma import eLabel, eSize, gFont
    from Components.MultiContent import MultiContentEntryText
    text = Path(filename).read_text(encoding='utf-8', errors='replace')
    widget = screen['Changelog_info']
    probe = eLabel(widget.instance)
    probe.hide()
    probe.resize(eSize(32768, 96))
    probe.setNoWrap(1)
    width = max(100, widget.instance.size().width() - 68)
    current_font = [None]
    def measure(value, heading):
        if current_font[0] != heading:
            probe.setFont(gFont('Prive3', 33 if heading else 30))
            current_font[0] = heading
        probe.setText(value)
        return probe.calculateSize().width()
    try:
        rows = layout(text, measure, width)
    finally:
        probe = None
    if not rows:
        return False
    screen.list = []
    for kind, value in rows:
        item = [value]
        if kind == 'rule':
            item.append(MultiContentEntryText(pos=(16, 17), size=(width, 2), font=0,
                text=' ', color=0x285870, backcolor=0x285870))
        elif kind != 'gap':
            item.append(MultiContentEntryText(pos=(16, 0), size=(width, 35),
                font=2 if kind == 'heading' else 0, text=value,
                color=0x3ee8ff if kind == 'heading' else 0xeeeeee))
        screen.list.append(item)
    widget.l.setList(screen.list)
    widget.selectionEnabled(0)
    return True
