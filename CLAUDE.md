# Odyssey Ebook — Michael Caine / ElevenLabs Edition

## Project Purpose
This is a fork of the Standard Ebooks William Cullen Bryant translation of Homer's Odyssey. The goal is to substitute Latinised/Roman character names with their Greek equivalents, to match the naming conventions used consistently in the ElevenLabs AI audiobook narrated via Michael Caine's voice clone (released June 2026).

## Directory Layout

```
epub-src/    ← SE project root; pass this to se lint / se build
scripts/     ← name-substitution Python scripts and data
new-cover/   ← working folder for new cover design
```

SE commands are run from the repo root with `epub-src/` as the project path:

```bash
se lint epub-src/
se build epub-src/
```

## Source Files
All content lives in `epub-src/src/epub/text/` as `book-1.xhtml` … `book-24.xhtml`, plus `introduction.xhtml` (the prose introduction — an Eleven Productions original transcribed from the audiobook, placed in the front matter, not numbered as a book), `preface.xhtml`, `colophon.xhtml`, etc. These are UTF-8 XHTML files containing typographic characters (`’`, `—`, curly quotes) — edits must preserve valid XHTML markup. Only modify metadata files like `content.opf` or `toc.xhtml` insofar as needed to reflect edits to `book-x.xhtml` files.

Verse is marked up cleanly: each poetic line is its own `<span>…</span>` separated by `<br/>`. Each book opens with a prose "argument" `<p>` that also contains names. The sole prose exception is `introduction.xhtml`, which is plain prose (ordinary `<p>` paragraphs) and has no argument.

## Name Substitution Map
The final, audio-verified swap list is documented in `README.md`. The mapping itself lives in `scripts/substitutions.json` and is applied by `scripts/substitute.py`; `scripts/extract_names.py` re-scans the books to confirm no Bryant forms remain.

- `scripts/substitute.py` is word-boundary-safe and **text-node-only** (tags, attributes, and whitespace pass through byte-for-byte). Dry-run by default; `--apply` writes in place as UTF-8 with original line endings preserved.
- `scripts/extract_names.py epub-src/src/epub/text` extracts proper-noun candidates into `scripts/names_report.md` / `scripts/names_raw_forms.csv` (gitignored). Dependency: `lxml`.

## Critical Traps
- **Bryant already mixes Greek and Roman.** Forms like `Hermes` and `Apollo` already appear in the source, so **never do a loose global replace** — substitute specific forms with word boundaries, longest / compound / possessive form first (e.g. `Pallas Athene` before bare `Pallas`, `Jove’s` before `Jove`).
- **The ElevenLabs narration only replaces the names of the 7 core deities** rather than all Roman names. Always ask for a human verification against the audio before doing a substitution. 
- **Encoding:** on Windows, always pass `encoding="utf-8"` to every `open()` for read AND write, or the `’`/`—` characters throw `charmap` errors and corrupt the typography. `PYTHONUTF8=1` is a safe global fallback.

## Completion status (as of 2026-06-29)

All substitution work is **complete**:
- All 24 book XHTML files have been updated (commit 5026a71).
- `toc.xhtml` entries mirror each book's `<p epub:type="title">` (Athena/Odysseus).
- `se:long-description` blurb in `content.opf` reads Odysseus/Poseidon (a third paragraph describing this edition was added later — see *Front/back matter restructure* below). Note: `dc:publisher`, `dc:source`, `se:url.vcs.github`, and `a11y:certifiedBy` were **subsequently repointed to this fork** in the restructure below; only the upstream `dc:identifier` and dates are still left as-is.
- `epub-src/src/epub/text/endnotes.xhtml` was added explaining every name change and every name deliberately kept as Bryant wrote it.

Do not re-run substitutions — the books are already in their final Greek-names state.

### Introduction added (2026-06-30, restructured 2026-07-01)
- `epub-src/src/epub/text/introduction.xhtml` adds the audiobook's framing introduction (opening "This is an Eleven Productions original."), transcribed from the Michael Caine narration. It is **prose, not verse**, titled simply "Introduction" (`<h2>Introduction</h2>`, no `se:label`/ordinal, no `p epub:type="title"`).
- It is **front matter, not a numbered book**: `epub:type="introduction"` in `frontmatter`. Spine + TOC slot is **after `note.xhtml` (the editor's note), before `halftitlepage.xhtml`**. Manifest item id `introduction.xhtml`; the `bodymatter` landmark now points to `book-1.xhtml`.
- Originally added as "Book 0" (`book-0.xhtml`); renamed and moved out of the books list on 2026-07-01 because it isn't one of the 24 books. Endnote 21 (in `endnotes.xhtml`, ref in `introduction.xhtml`) explains it is not part of Homer's poem.
- It is new content that already uses the Greek names (Odysseus), not a Bryant passage, so it is **exempt from the substitution scripts** — `extract_names.py` may surface its forms, but do not run `substitute.py` against it.

### Front/back matter restructure (2026-06-30)
The front/back matter was reorganized so the book reads as a fork, not a Standard Ebooks edition:
- **Editor's note added** — `text/note.xhtml` ("About This Edition", `epub:type="preface"`, `frontmatter`), signed "Stoil M. Stoilov, July, 2026." Explains the Greek-name restoration, the metre caveat, and the preface relocation. Spine slot: after `imprint.xhtml`, before `halftitlepage.xhtml`; TOC front-matter entry "About This Edition".
- **Bryant's preface relocated to the back** — `text/preface.xhtml` is unchanged in body text but is now `epub:type="afterword"` / `backmatter`, heading retitled "W. C. Bryant's Preface to His Translation (1871)". Spine: moved to after `book-24.xhtml`, before `endnotes.xhtml`; TOC back-matter entry before Endnotes.
- **Colophon rewritten + de-branded** — `text/colophon.xhtml`: SE publisher `logo.svg` removed (its manifest item lost `properties="svg"`); records the factual Standard Ebooks → public-domain page-scan lineage (**no Project Gutenberg** — SE's own page lists only Internet Archive / HathiTrust / Google Books scans), the modifications, the editor + year 2026, and the CC0 dedication.
- **`content.opf` metadata** — added editor contributor `Stoil Miroslavov Stoilov` (role `edt`); `dc:publisher` and `a11y:certifiedBy` changed from "Standard Ebooks" to the editor; `se:url.vcs.github` and the publisher homepage repointed to the fork (`github.com/sstoilovABLE/…`); SE edition URL added to `dc:source`; `dc:description` + `se:long-description` rewritten for this edition. `dc:identifier` and dates left upstream (see TASKS.md).
- Still TODO (see TASKS.md): de-brand the **cover**, **title page**, and **imprint** (these still carry SE branding/`logo.svg`); regenerate plumbing with `se`; lint; build.

These files contain Bryant/Roman forms **on purpose** — never run `substitute.py` against them:
- `note.xhtml` — the editor's note quotes the Roman names ("Ulysses, Neptune, Minerva, Jove") to explain the change. New content; exempt from the substitution scripts.
- `preface.xhtml` — Bryant's 1871 preface arguing *for* keeping the Latin names; swapping would make it self-contradictory.
- `endnotes.xhtml` — quotes the Bryant forms to explain each change.
- `colophon.xhtml` — names the Roman forms when describing the change, and keeps "Ulysses and the Sirens," the actual title of the Waterhouse painting.

## Critical Caveat — Metre
Bryant wrote in blank verse (iambic pentameter). Roman and Greek names are often NOT syllable-equivalent. Substitutions WILL break metre in many lines. This is accepted and intentional for this edition — the goal is name consistency with the audio, not metrical perfection. Do NOT attempt to repair metre.

## Approach
- Preserve all XHTML tags exactly
- Preserve capitalisation (e.g. "Ulysses" → "Odysseus", "ULYSSES" → "ODYSSEUS")
- Handle possessives (e.g. "Ulysses'" → "Odysseus'")
- Do NOT substitute inside XML attributes, only inside text nodes
- Regularly update README.md and CLAUDE.md to keep them up-to-date
- After every run, update TASKS.md to reflect tasks completed and to potentially add new tasks that may need to be done