#!/usr/bin/env python3
"""
Tier 2: apply the Roman -> Greek name substitutions in substitutions.json to the
Bryant Odyssey book files, so the text matches the ElevenLabs / Michael Caine
narration.

Design notes
------------
* TEXT NODES ONLY. The file is split into markup tokens (tags, comments, CDATA,
  the XML declaration) and text runs; substitutions touch only the text runs, so
  tags, attributes and all other markup are passed through byte-for-byte. No XML
  parser/serialiser is used, which means <br/>, attribute quoting, namespaces and
  typographic characters are never reformatted.
* WORD BOUNDARIES. Every form is matched with \\b...\\b (or \\b...(?!\\w) for the
  bare-apostrophe possessives), so Greek names already in Bryant -- Hermes,
  Apollo, Hades, Ares -- are never touched, and no name is matched inside a longer
  word.
* IN ORDER. Entries are applied in the order they appear in substitutions.json,
  which is arranged longest / compound / possessive form first -- so
  "Pallas Athene" resolves before bare "Pallas", and "Jove’s" before "Jove".
* CASE. Each form is applied in its canonical (title) case and in ALL-CAPS. The
  current text contains no all-caps name forms, so the upper-case variants simply
  report zero; they are kept as cheap insurance per the project's capitalisation
  rule (ULYSSES -> ODYSSEUS).
* ENCODING. Files are read and written as UTF-8 with newline="" so the original
  line endings and every curly quote / em-dash survive untouched.

Usage
-----
    python tools/substitute.py                 # DRY RUN on src/epub/text (default)
    python tools/substitute.py --apply         # write the changes in place
    python tools/substitute.py path/to/text --apply
    python tools/substitute.py --json tools/substitutions.json --apply

After --apply, re-run:  python tools/extract_names.py src/epub/text
and confirm Section A is empty (no Bryant forms remain).
"""
import sys
import os
import re
import glob
import json

# Resolve defaults relative to this script (which lives in tools/), not the cwd,
# so the tool works no matter where it is invoked from.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
DEFAULT_TEXT_DIR = os.path.join(_ROOT, "src", "epub", "text")
DEFAULT_JSON = os.path.join(_HERE, "substitutions.json")

# Split a document into markup and text. Order matters: comments and CDATA are
# matched before the generic tag rule (they may contain quotes or > characters),
# and the tag rule is quote-aware so a > inside an attribute value can't end a tag
# early. Any token that does NOT start with "<" is a text run and is the only
# thing we ever rewrite.
TOKEN_RE = re.compile(
    r"<!--.*?-->"                      # comments
    r"|<!\[CDATA\[.*?\]\]>"            # CDATA sections
    r"|<(?:\"[^\"]*\"|'[^']*'|[^>])*>"  # tags / declarations / PIs (quote-aware)
    r"|[^<]+",                          # text run
    re.DOTALL,
)

# Apostrophe class: the source uses U+2019, but we accept ASCII ' too so a stray
# straight quote can't silently slip a possessive past us.
APOS = "[’']"


def load_entries(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Applied in file order: the JSON is already arranged longest / compound /
    # possessive form first (e.g. "Pallas Athene" before "Pallas").
    return data["substitutions"]


def build_rules(entries):
    """Expand each entry into (label, compiled_pattern, replacement) rules,
    one for the canonical case and one for ALL-CAPS."""
    rules = []
    seen = set()
    for e in entries:
        frm, to = e["from"], e["to"]
        for f, t in ((frm, to), (frm.upper(), to.upper())):
            if f in seen:
                continue
            seen.add(f)
            # Rebuild the pattern from the literal form but make the apostrophe
            # flexible (U+2019 or ASCII ').
            core = re.escape(f).replace(re.escape("’"), APOS)
            if f[-1].isalnum():
                right = r"\b"
            else:                       # form ends in an apostrophe (possessive)
                right = r"(?!\w)"
            pattern = re.compile(r"\b" + core + right)
            rules.append((f, t, pattern))
    return rules


def substitute_text(text, rules, counts):
    """Apply every rule to one text run; tally hits into counts[label]."""
    for label, repl, pattern in rules:
        text, n = pattern.subn(lambda m, r=repl: r, text)
        if n:
            counts[label] = counts.get(label, 0) + n
    return text


def process_document(src, rules):
    """Return (new_text, counts) for a whole file, rewriting text runs only."""
    counts = {}
    out = []
    for tok in TOKEN_RE.finditer(src):
        s = tok.group(0)
        if s.startswith("<"):
            out.append(s)                       # markup: untouched
        else:
            out.append(substitute_text(s, rules, counts))
    return "".join(out), counts


def main(argv):
    # Windows consoles often use a non-UTF-8 code page (cp1251/cp1252); make
    # stdout tolerant so printing a name like "Pallas Athenè" can't crash the
    # run. File reads/writes are always UTF-8 regardless of this.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    apply = False
    json_path = DEFAULT_JSON
    text_dir = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--apply":
            apply = True
        elif a == "--json":
            i += 1
            json_path = argv[i]
        elif a.startswith("--"):
            sys.exit(f"Unknown option: {a}")
        else:
            text_dir = a
        i += 1
    if text_dir is None:
        text_dir = DEFAULT_TEXT_DIR

    entries = load_entries(json_path)
    rules = build_rules(entries)

    paths = sorted(
        glob.glob(os.path.join(text_dir, "book-*.xhtml")),
        key=lambda p: int(re.search(r"book-(\d+)", os.path.basename(p)).group(1)),
    )
    if not paths:
        sys.exit(f"No book-*.xhtml files found in {text_dir!r}")

    mode = "APPLY (writing in place)" if apply else "DRY RUN (no files written)"
    print(f"substitute.py -- {mode}")
    print(f"  text dir : {text_dir}")
    print(f"  map      : {json_path}  ({len(entries)} forms, {len(rules)} case variants)")
    print("=" * 60)

    grand = {}
    files_changed = 0
    for path in paths:
        with open(path, "r", encoding="utf-8", newline="") as f:
            src = f.read()
        new, counts = process_document(src, rules)
        total = sum(counts.values())
        if total:
            files_changed += 1
            print(f"\n{os.path.basename(path)}  ({total} replacements)")
            # report in the same longest-first order as the rules
            for label, _repl, _pat in rules:
                if label in counts:
                    arrow = next(t for (f, t, _p) in rules if f == label)
                    print(f"    {label:<12} -> {arrow:<12} {counts[label]:>4}")
                    grand[label] = grand.get(label, 0) + counts[label]
        if apply and new != src:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)

    print("\n" + "=" * 60)
    print(f"{'TOTAL':<26}{sum(grand.values()):>6} replacements in {files_changed} files")

    # Sanity: any canonical form that matched nowhere is suspicious.
    canon = [e["from"] for e in entries]
    missing = [c for c in canon if c not in grand]
    if missing:
        print("\nNOTE: these forms matched in zero files (check if expected):")
        print("  " + ", ".join(missing))

    if not apply:
        print("\nThis was a DRY RUN. Re-run with --apply to write the changes.")


if __name__ == "__main__":
    main(sys.argv[1:])
