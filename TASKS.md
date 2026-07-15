# 📋 Project Task Tracker

- [x] Update LICENSE.md
- [x] Add .gitignore
- [x] Create script to extract Roman name occurrences from the original WCB translation epub files
- [x] Add README.md
- [x] Create script to substitute Roman names with Greek ones
- [x] Create substitution table JSON with Roman names and Greek equivalents
- [x] Substitute Roman names with Greek ones, insofar as needed to match the Michael Caine narration
- [x] Create/update CLAUDE.md
- [x] Reorganize project directory to be cleaner
- [x] Create Chapter 0 from the Michael Caine narration
- [x] Write Editor's Note for the front and move WCB Preface to the end
    - [x] Rewrite colophon.xhtml (de-brand, factual lineage, record modifications, name editor)
    - [x] Update content.opf metadata (editor contributor, de-brand publisher/VCS, source, descriptions)
- [x] Write an endnote for the bridgehead section at the beginning of each book - explain it is not read out by Michael Caine but is kept for context and authenticity (added as note-1 on Book 1's bridgehead only; existing name-notes renumbered 2–20)
- [x] Renamed "Book 0" to a front-matter "Introduction" (`introduction.xhtml`, placed after the editor's note and before the half-title page; dropped the `se:label`/ordinal and `p` title; updated content.opf, toc.xhtml, colophon, README, CLAUDE.md)
- [x] Write an endnote for the Introduction - explain it is not in the original Odyssey but added to match the ElevenLabs narration
- [x] Fix Book 1 bridgehead: Bryant's argument said Athena appeared "in the shape of Mentor," but Book 1's own text has her as Mentes (Mentor is a distinct character, impersonated by Athena only later, in Books 2, 22, and 24) — corrected the argument to "Mentes" and added an explanatory endnote (new note-2; all subsequent notes renumbered up by one, now 1–22). This is an editorial correction of a Bryant slip, unrelated to the Greek/Roman deity-name substitution project — not run through `substitute.py`.
- [x] Create new book cover; remove Standard Ebooks branding/wordmark from it (added in commit 8253014; wired up as the actual `cover-image` in this pass — see below)
- [x] Wire the new cover art into the EPUB: `cover.svg` is now a self-contained SVG wrapper embedding the new art as a JPEG (resized to the SE-standard 1400×2100 to stay under the 4,000,000-pixel limit; ~348 KB JPEG / ~464 KB SVG, replacing the 3.6 MB PNG). Keeps the `properties="cover-image"` slot; de-branded the SVG `<title>`.
- [x] De-brand the title page (titlepage.xhtml): dropped the SE `titlepage.svg` wordmark, now shows the new cover art plus visible plain-text credits (author, translator, and editor); `local.css` linked after `se.css` with an override that un-hides the titlepage credits (registered in `se-lint-ignore.xml`).
- [x] De-brand the imprint (imprint.xhtml): removed the SE logo and reworded the page as an unofficial derivative work based on the Standard Ebooks edition (context drawn from the Editor's Note and README); kept the source, page-scans, CC0, and Uncopyright links.
- [x] Remove images/logo.svg from the manifest and delete it (nothing references it now); also deleted the now-unused images/titlepage.svg. Recorded the intentional `f-002` (missing logo.svg) and `s-028` (no titlepage SVG to match) deviations in `se-lint-ignore.xml`.
- [x] Revisit colophon cover-art credits: the cover no longer derives from Waterhouse's *Ulysses and the Sirens*, so the credit now reads "designed for this edition by Stoil M. Stoilov, adapted from the cover art of the ElevenReader audiobook," and the licence line notes the cover image is not dedicated to the public domain. (No typeface credit exists in the colophon; The League of Moveable Type remains in content.opf as the SE body-font designer, which still applies.)
- [x] Decide whether to mint a new dc:identifier and update dc:date for this fork edition — minted a fork-specific `dc:identifier` (`https://github.com/sstoilovABLE/odyssey-ebook-michael-caine-elevenlabs-narration`, replacing the upstream SE URL) and set `dc:date` + `dcterms:modified` to 2026-07-15. This also flips SE's `is_se_ebook` detection off, which correctly disables the SE-house-style lints a fork shouldn't be held to (f-002 logo, f-003 uncopyright boilerplate, m-035 SE-identifier-in-colophon, m-075 page-scans link).
- [x] Review the "Standard Ebooks makes no representations" line in uncopyright.xhtml — already reworded to "The editor of this edition makes no representations…"; verified and left as-is (f-003 no longer needs an ignore rule since the SE boilerplate check is off for a non-SE identifier).
- [x] Update word count and other metadata — `se prepare-release --no-revision` recomputed `schema:wordCount` (120292) and `schema:educationalLevel` (71.28) (m-065); added `schema:accessMode` visual (m-028) and a `wat` alt-text-writer role on the editor (m-040). Also added `win` (writer of introduction, editor as transcriber), `ann` (annotator/endnotes, editor), and `wpr` (preface = the editor's note) roles, and changed Bryant's stale `wpr` to `waw` (his preface is now the afterword) — clearing m-030/m-032/m-033. Editor relators reordered alphabetically (m-087).
- [x] Run se lint; fix/triage remaining warnings and errors — **`se lint epub-src/` is now clean (exit 0)**. Fixed: s-032 (removed invalid `epub:type="endnote"` from all 22 endnote `<li>`s — se 4.0 drops it), s-001 (`&#239;` → literal `ï` in note.xhtml), m-042 (regenerated `<manifest>`), the colophon m-041/m-061/s-106 (link text "HathiTrust Digital Library", "the" before the source links, wrapped "Stoil M. Stoilov" in `<b epub:type="z3998:personal-name">`), plus the metadata items above. Intentional divergences recorded in `se-lint-ignore.xml`: m-009 (VCS URL points to the real fork repo) and t-061 (Bryant's summary-style bridgeheads intentionally lack terminal punctuation). Retained the pre-existing c-009 (local.css) and s-028 (no titlepage SVG) ignores.
- [x] Regenerate manifest/spine/TOC with se tooling and verify landmarks — regenerated the manifest with `se build-manifest`. Diffed `se build-spine`/`se build-toc` output against the current files: the sole content differences were (a) SE's canonical order would swap the editor's note and the introduction, which this edition **intentionally** keeps as note→introduction (kept the current spine/TOC order), and (b) a missing backmatter landmark — added the `endnotes` landmark to the TOC. Verified the bodymatter landmark points to book-1.xhtml.
- [x] Build EPUB — `se build --output-dir dist/ epub-src/` succeeds; the output is epubcheck-valid (0 fatals / 0 errors / 0 warnings, EPUB 3.3) and ~1 MB. Note: `se build --check` throws a spurious "Couldn't parse XML" error in the CI/proxy env because Java's `JAVA_TOOL_OPTIONS` banner pollutes the stream `se` parses; running `se build` bare and then epubcheck directly validates clean. Also note `se` now names the output file after the `dc:identifier` (the GitHub URL), so rename it for distribution.
- [x] Test on Google Play Books and Calibre ebook reader — tested on Google Play Books: works excellently.
- [x] Compile final v1.0 EPUB — v1.0 built and tagged in the colophon (`the-odyssey-greek-names-caine-edition.epub`, the compatibility build). Still pending (maintainer): uploading the v1.0 EPUB to GitHub Releases.


# Actions to be done after every task

- Update README.md and CLAUDE.md only after significant tasks that concern the whole project — not after small or narrowly-scoped fixes
- Update TASKS.md to reflect tasks completed and to potentially add new tasks that may need to be done
