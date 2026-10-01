# Slides archive

Upload source PDFs to `raw/`. This directory stays local and is excluded from both Git and Jekyll.

Public talk and defense slides live in `slides/` with names such as
`2026-07-22-dpf-jinchen-he.pdf`: presentation date, event, presenter, lowercase ASCII separated by hyphens. Use only a year or month when a full date is unknown. Preserve distinct presentations of the same research at different events.

Compare SHA-256 before deduplicating. Inspect the title page to match the event; filenames alone are insufficient. In particular, the uploaded `candidacy_talk.pdf` is identical to the April 2025 Nuclear Theory Seminar slides and is archived under that event.

The current archive's original names, canonical names, and hashes are recorded in `slides-archive.json`. All website and CV talk-list references use the canonical names. Renaming changes previously shared PDF URLs; this archive does not retain duplicate copies under old names.

Posters remain separate from slides. The NeurIPS 2025 poster is already published at `notes/NIPS_ml4ps_2025.pdf` and linked from Publications; its duplicate upload was removed after hash verification.

Before publishing, check every local PDF link, build the website with `bash run_build.sh`, and synchronize `../Jinchen_CV/TALKS.md`. Rebuild all CVs and copy the academic English PDF to `notes/Jinchen_CV_updated.pdf` whenever CV sources change.

The SciDAC 2026 PI Meeting poster is archived separately as `notes/2026-08-scidac-poster-jinchen-he.pdf`. Its August 4–6 date range describes the meeting, not a separately confirmed personal presentation date. The LaMET 2024 talk date is August 14, 2024, verified against the official contribution record; the PDF title page retains its original July label.

The April 15, 2026 Student Lunch Talk at Argonne National Laboratory is published as `slides/2026-04-15-argonne-student-lunch-jinchen-he.pdf`. Its Slides link is shared by the website talk record and the CV repository talk list; no event webpage was provided.
