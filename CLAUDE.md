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
- **`content.opf` metadata** — added editor contributor `Stoil Miroslavov Stoilov` (role `edt`); `dc:publisher` and `a11y:certifiedBy` changed from "Standard Ebooks" to the editor; `se:url.vcs.github` and the publisher homepage repointed to the fork (`github.com/stoilms/…`); SE edition URL added to `dc:source`; `dc:description` + `se:long-description` rewritten for this edition. `dc:identifier` and dates left upstream (see TASKS.md).
- The **cover**, **title page**, and **imprint** were subsequently de-branded — see *Cover & branding finalized* below. Still TODO (see TASKS.md): remaining metadata (`dc:identifier`/dates, word count, `schema:accessMode`/`wat` role), triage of the remaining pre-existing `se lint` errors, regenerate plumbing with `se`, and the final build/release.

These files contain Bryant/Roman forms **on purpose** — never run `substitute.py` against them:
- `note.xhtml` — the editor's note quotes the Roman names ("Ulysses, Neptune, Minerva, Jove") to explain the change. New content; exempt from the substitution scripts.
- `preface.xhtml` — Bryant's 1871 preface arguing *for* keeping the Latin names; swapping would make it self-contradictory.
- `endnotes.xhtml` — quotes the Bryant forms to explain each change.
- `colophon.xhtml` — names the Roman forms (Ulysses/Neptune/Minerva/Jove) when describing the change. (The old Waterhouse *Ulysses and the Sirens* cover credit was removed when the cover was replaced — see *Cover & branding finalized* below.)

### Cover & branding finalized (2026-07-15)
The new cover art (added in commit 8253014 as `images/cover-new.png`, matching the ElevenReader audiobook cover — see README for its copyright status) was wired up as the real cover, and the last SE branding was removed from the front matter:
- **Cover** — `images/cover.svg` is now a self-contained SVG wrapper embedding the new art as a JPEG. The art was resized to the SE-standard **1400×2100** (the 1667×2500 source exceeded the 4,000,000-pixel `f-018` limit) and compressed to JPEG (~348 KB), so `cover.svg` is ~464 KB and the whole EPUB is ~1 MB (vs. ~4.4 MB with the raw PNG). Keeps `properties="cover-image"`; the SVG `<title>` was de-branded. `images/cover-new.jpg` is the same JPEG, referenced by the title page. The 3.6 MB `cover-new.png` was deleted from `images/` (the original still lives in `new-cover/ebook-cover-updated.png`).
- **Title page** (`titlepage.xhtml`) — dropped the SE `titlepage.svg` wordmark; now shows the cover art (`cover-new.jpg`) plus **visible** plain-text credits (By Homer / Translated by Bryant / Edited by Stoil M. Stoilov). SE's `se.css` hides titlepage `h1`/`p` off-screen, so `local.css` is now linked **after** `se.css` on this page with an override that un-hides the `p` credits (with `text-indent: 0` to satisfy `c-011`); the `h1` stays hidden since the art carries the title.
- **Imprint** (`imprint.xhtml`) — removed the SE `z3998:publisher-logo` image and its `<header>`; reworded (drawing on the Editor's Note and README) as an unofficial derivative work based on the Standard Ebooks edition, keeping the source / page-scans / CC0 / Uncopyright links and noting the cover-image copyright exception. Lost `properties="svg"` in the manifest.
- **Colophon** (`colophon.xhtml`) — cover-art credit rewritten (no longer Waterhouse); licence line notes the cover is not public domain.
- **Deleted files** — `images/logo.svg` and `images/titlepage.svg` removed from disk and manifest. `content.opf` manifest now lists only `cover.svg` + `cover-new.jpg` under images; the Waterhouse `art` contributor was already gone (commit 8253014).
- **Linting** — cover/image/branding lints are clean. Intentional SE-conformance deviations are recorded in `epub-src/se-lint-ignore.xml`: `s-028` (no titlepage SVG to match the cover SVG) and `f-002` (SE `logo.svg` removed; `LICENSE.md` lives at the repo root). The remaining `se lint` errors are all pre-existing and tracked in TASKS.md. `se build epub-src/` succeeds (epubcheck-valid).
- **These are new/branding content — exempt from the substitution scripts** (like the other front/back matter): `titlepage.xhtml`, `imprint.xhtml`, `colophon.xhtml`.

### Metadata & lint finalized (2026-07-15)
`se lint epub-src/` is now **clean (exit 0)**, and all metadata/plumbing tasks short of the final build are done.
- **Fork identifier + dates** — `dc:identifier` is now the fork's GitHub URL (was the upstream SE ebook URL); `dc:date` and `dcterms:modified` are 2026-07-15. Because the identifier is no longer a `standardebooks.org` URL, SE's `is_se_ebook` detection is off, which correctly **disables the SE-house-style lints a fork shouldn't be held to** (f-002 logo, f-003 uncopyright boilerplate, m-035 SE-identifier-in-colophon, m-075 page-scans link). The old f-002/f-003 ignore rules were therefore removed as unused.
- **MARC relators** — the editor (Stoil M. Stoilov) now carries `ann` (annotator/endnotes), `edt`, `wat` (alt-text writer), `win` (writer of introduction — as its transcriber), and `wpr` (writer of preface — the "About This Edition" editor's note is the `preface` semantic); listed alphabetically. Bryant's stale `wpr` became `waw` (his original preface is now the `afterword`). This cleared m-030/m-032/m-033/m-040/m-087.
- **Word count / accessibility** — `se prepare-release --no-revision` recomputed `schema:wordCount` (120292) and `schema:educationalLevel` (71.28) (m-065). Added `schema:accessMode` `visual` (m-028). Note: `se`'s metadata-normalization step strips a manually-added second `schema:accessMode`, so re-add it **after** running `prepare-release`/`build-manifest` if those are re-run.
- **XHTML fixes** — removed the now-invalid `epub:type="endnote"` from all 22 endnote `<li>`s (se 4.0 dropped that value; the plural `endnotes` on the section stays) (s-032); replaced `&#239;` with a literal `ï` in `note.xhtml` (s-001); regenerated `<manifest>` with `se build-manifest` (m-042).
- **Colophon** — link text now "HathiTrust Digital Library" (m-041); "the" precedes the Internet Archive and HathiTrust source links (m-061); "Stoil M. Stoilov" wrapped in `<b epub:type="z3998:personal-name">` at both by-lines (s-106). These are still exempt from `substitute.py`.
- **Spine / TOC / landmarks** — manifest regenerated. `se build-spine`/`build-toc` would reorder the editor's note and the introduction into SE's canonical order; this edition **intentionally** keeps note→introduction, so the spine/TOC order was left as-is. Added the missing `endnotes` backmatter landmark to `toc.xhtml`; the bodymatter landmark points to `book-1.xhtml`.
- **`se-lint-ignore.xml`** now records only genuine fork divergences: `c-009` (local.css bridgehead overrides), `s-028` (no titlepage SVG), `m-009` (VCS URL is the real fork repo), and `t-061` (Bryant's summary-style bridgeheads intentionally lack terminal punctuation).
- **Still TODO** (deferred to the maintainer): final `se build epub-src/`, testing on Google Play Books / Calibre, and compiling + uploading the v1.0 EPUB to Releases.

## Critical Caveat — Metre
Bryant wrote in blank verse (iambic pentameter). Roman and Greek names are often NOT syllable-equivalent. Substitutions WILL break metre in many lines. This is accepted and intentional for this edition — the goal is name consistency with the audio, not metrical perfection. Do NOT attempt to repair metre.

## Approach
- Preserve all XHTML tags exactly
- Preserve capitalisation (e.g. "Ulysses" → "Odysseus", "ULYSSES" → "ODYSSEUS")
- Handle possessives (e.g. "Ulysses'" → "Odysseus'")
- Do NOT substitute inside XML attributes, only inside text nodes
- Only update README.md and CLAUDE.md after significant tasks that concern the whole project (e.g. structural changes, new front/back matter, completion milestones) — not after small or narrowly-scoped fixes (e.g. a single typo/inconsistency correction).
- After every run, update TASKS.md to reflect tasks completed and to potentially add new tasks that may need to be done