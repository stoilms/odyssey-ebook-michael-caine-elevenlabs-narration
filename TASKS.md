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
- [ ] Decide whether to mint a new dc:identifier and update dc:date for this fork edition
- [ ] Review the "Standard Ebooks makes no representations" line in uncopyright.xhtml
- [ ] Update word count and other metadata (`se lint` m-065; also add `schema:accessMode` visual (m-028) and a `wat` alt-text-writer role (m-040) now that in-content images have alt text)
- [ ] Run se lint; fix/triage remaining warnings and errors. Cover/image/branding lints are now clean; the remaining errors are pre-existing and belong to the metadata items above and to the SE-conformance lints a fork intentionally diverges from (colophon lineage m-035/m-041/m-061/m-075/s-106, VCS-URL m-009, manifest-structure m-042, m-030/m-032/m-033, s-001, s-032, t-061).
- [ ] Regenerate manifest/spine/TOC with se tooling and verify landmarks
- [ ] Build EPUB (`se build epub-src/` currently succeeds — epubcheck-valid, ~1 MB — this remains for the final v1.0 build)
- [ ] Test on Google Play Books and Calibre ebook reader
- [ ] Compile final v1.0 EPUB and upload it to Releases


# Actions to be done after every task

- Update README.md and CLAUDE.md only after significant tasks that concern the whole project — not after small or narrowly-scoped fixes
- Update TASKS.md to reflect tasks completed and to potentially add new tasks that may need to be done
