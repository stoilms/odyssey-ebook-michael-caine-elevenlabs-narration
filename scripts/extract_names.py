#!/usr/bin/env python3
"""
Tier 1: extract every proper-noun candidate from the Standard Ebooks
William Cullen Bryant translation of the Odyssey.

Key trick: Bryant is blank verse, and each verse line is wrapped in its own
<span> in the SE markup. Verse convention capitalises the FIRST word of every
line regardless of grammar, so a capitalised word that is *line-initial* tells
us nothing. A capitalised word that appears *mid-line* is a high-confidence
proper noun. We track both, plus possessive/adjectival forms, and flag any
token matching the known Roman->Greek substitution set.

Usage: python tools/extract_names.py src/epub/text
Outputs: names_report.md, names_raw_forms.csv  (written next to this script, in tools/)
"""
import sys, re, glob, os, csv
from collections import defaultdict
from lxml import etree

# Anchor defaults/outputs to this script (in tools/), not the cwd, so the tool
# works from any directory and never litters the repo root with its reports.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
TEXT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, "src", "epub", "text")

# The FINAL audio-verified Roman->Greek swaps — the ONLY names the ElevenLabs /
# Michael Caine narration changes from Bryant. Used to FLAG, not to limit
# extraction. After `substitute.py --apply` these should all be gone, so a clean
# pass shows an EMPTY Section A. (All other Latinate names — Minerva, Venus,
# Vulcan, Diana, Ceres, Latona, Mars, Pluto, Proserpine, Bacchus, Phoebus,
# Aurora — are kept in the narration and so are intentionally absent here.)
ROMAN_TO_GREEK = {
    "Ulysses": "Odysseus", "Jove": "Zeus", "Jupiter": "Zeus",
    "Neptune": "Poseidon", "Saturn": "Cronos", "Juno": "Hera",
    "Mercury": "Hermes", "Pallas": "Athena",
}

# Common words that get capitalised mid-line for non-name reasons.
# (Interjections, "O" address, deified common nouns we may or may not care about.)
STOPCAPS = {"O", "I", "Ah", "Oh", "Lo", "Nay", "Yea", "Hail", "But", "And",
            "Then", "Now", "Thou", "Thee", "Thy", "Ye", "He", "She", "We",
            "They", "It", "His", "Her", "My", "Their", "When", "Where",
            "While", "Yet", "For", "So", "If", "As", "Though", "Madmen"}

WORD_RE = re.compile(r"[A-Za-z][A-Za-z\u2019'\-]*")

# strip a trailing possessive: Jove’s / Jove's -> Jove ; Achilles’ -> Achilles
def base_form(tok):
    t = tok.strip("’'\u2019-")
    t = re.sub(r"[’'\u2019]s$", "", t)   # 's
    t = re.sub(r"[’'\u2019]$", "", t)    # trailing ' (plural possessive)
    return t

NS = {"x": "http://www.w3.org/1999/xhtml"}

# midline_count[base] / initial_count[base] ; raw_forms[base] = set of literal forms seen
midline = defaultdict(int)
initial = defaultdict(int)
raw_forms = defaultdict(set)
form_books = defaultdict(set)  # base -> set of book numbers

def book_num(path):
    m = re.search(r"book-(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0

def process_line(text, bk, is_verse_line):
    """Tokenise one unit. In a verse line the first word is line-initial.
    In prose we approximate sentence-initial by position after . ! ? :"""
    toks = list(WORD_RE.finditer(text))
    for i, m in enumerate(toks):
        tok = m.group(0)
        if not tok[0].isupper():
            continue
        b = base_form(tok)
        if not b or b in STOPCAPS:
            continue
        # determine if this token is "initial"
        is_initial = (i == 0)
        if not is_verse_line and i > 0:
            # prose: check char before the token for sentence-ending punct
            start = m.start()
            preceding = text[:start].rstrip()
            if preceding and preceding[-1] in ".!?:":
                is_initial = True
        if is_initial:
            initial[b] += 1
        else:
            midline[b] += 1
        raw_forms[b].add(tok)
        form_books[b].add(bk)

for path in sorted(glob.glob(os.path.join(TEXT_DIR, "book-*.xhtml")), key=book_num):
    bk = book_num(path)
    tree = etree.parse(path, etree.XMLParser(recover=True))
    # verse lines: <span> elements (each is one poetic line)
    for span in tree.iterfind(".//x:span", NS):
        # skip structural spans (labels, ordinals) — those have epub:type
        etype = span.get("{http://www.idpf.org/2007/ops}type")
        if etype:
            continue
        txt = "".join(span.itertext())
        if txt.strip():
            process_line(txt, bk, is_verse_line=True)
    # prose paragraphs (bridgeheads/arguments): <p> not containing spans
    for p in tree.iterfind(".//x:p", NS):
        if p.find(".//x:span", NS) is not None:
            continue
        ptype = p.get("{http://www.idpf.org/2007/ops}type")
        txt = "".join(p.itertext())
        if txt.strip():
            process_line(txt, bk, is_verse_line=False)

# A base is a confident proper noun if it appears mid-line at least once.
all_bases = set(midline) | set(initial)
confident = {b for b in all_bases if midline[b] > 0}
initial_only = {b for b in all_bases if midline[b] == 0}

def total(b):
    return midline[b] + initial[b]

# ---- write the human-readable report ----
with open(os.path.join(_HERE, "names_report.md"), "w", encoding="utf-8") as f:
    f.write("# Bryant Odyssey — proper-noun extraction (Tier 1)\n\n")

    f.write("## A. Substitution targets found (Roman names needing a Greek swap)\n\n")
    f.write("| Bryant form | → Greek | Total | Mid-line | Books | Raw forms seen |\n")
    f.write("|---|---|---|---|---|---|\n")
    for roman in sorted(ROMAN_TO_GREEK, key=lambda r: -total(r) if r in all_bases else 0):
        if roman in all_bases:
            forms = ", ".join(sorted(raw_forms[roman]))
            books = ",".join(str(x) for x in sorted(form_books[roman]))
            f.write(f"| {roman} | {ROMAN_TO_GREEK[roman]} | {total(roman)} | {midline[roman]} | {books} | {forms} |\n")
    f.write("\n*Not found in text:* " +
            ", ".join(sorted(r for r in ROMAN_TO_GREEK if r not in all_bases)) + "\n\n")

    f.write("## B. All confident proper nouns (appear mid-line ≥1), by frequency\n\n")
    f.write("| Name | Total | Mid-line | Line-initial | Raw forms |\n|---|---|---|---|---|\n")
    for b in sorted(confident, key=lambda x: -total(x)):
        forms = ", ".join(sorted(raw_forms[b]))
        f.write(f"| {b} | {total(b)} | {midline[b]} | {initial[b]} | {forms} |\n")

    f.write("\n## C. Capitalised-only-at-line-start (likely NOT names — review for missed ones)\n\n")
    f.write("These never appear mid-line, so they're probably ordinary words that happen to start verse lines. Skim for any real name hiding here.\n\n")
    f.write("| Token | Times | \n|---|---|\n")
    for b in sorted(initial_only, key=lambda x: -initial[x]):
        if initial[b] >= 2:  # filter singletons to keep it readable
            f.write(f"| {b} | {initial[b]} |\n")

# ---- write a raw-forms CSV for building regexes ----
with open(os.path.join(_HERE, "names_raw_forms.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["base", "is_substitution_target", "greek", "total", "midline", "raw_forms", "books"])
    for b in sorted(all_bases, key=lambda x: -total(x)):
        if total(b) < 1:
            continue
        is_target = b in ROMAN_TO_GREEK
        w.writerow([b, is_target, ROMAN_TO_GREEK.get(b, ""), total(b),
                    midline[b], "|".join(sorted(raw_forms[b])),
                    ",".join(str(x) for x in sorted(form_books[b]))])

print(f"Confident proper nouns: {len(confident)}")
print(f"Substitution targets found: {sum(1 for r in ROMAN_TO_GREEK if r in all_bases)}")
print("Wrote names_report.md and names_raw_forms.csv")
