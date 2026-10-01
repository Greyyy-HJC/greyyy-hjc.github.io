# INSPIRE publication synchronization

The bibliography source is the [official INSPIRE API](https://github.com/inspirehep/rest-api-doc), using author record [1935435](https://inspirehep.net/authors/1935435). The crawler resolves the author record's unique BAI (`Jinchen.He.1`) and fetches all matching literature records, including conference papers. It validates each record's author link, follows pagination, and checks the final count before replacing any output.

## Local update

```sh
python3 inspire_crawler/main.py
python3 -m unittest discover -s inspire_crawler -p 'test_*.py'
```

Python 3.9+ is sufficient; no pip dependencies or API credentials are required. The output is `_data/inspire_publications.json`. Commit an updated local snapshot when refreshing the static/no-JavaScript fallback. Never manually edit this generated file.

`_data/publication_extras.json` stores personal links keyed by INSPIRE literature record ID. Poster, Slides, repository and software links survive bibliography refreshes. It is maintained by hand; titles, authors, journal references, DOI, arXiv and citation counts come from INSPIRE. Missing citation counts are omitted, rather than shown as zero. Citation totals refer to INSPIRE, not Google Scholar.

## Scheduled website update

`.github/workflows/inspire_crawler.yaml` replaces the old Google Scholar workflow. It runs daily at 08:00 UTC, on relevant source changes to `main`, or on manual dispatch. It publishes `inspire_data.json` to the `inspire-stats` branch with normal commits, without force-pushing or changing the website source branch. GitHub Actions needs repository Contents write permission. The old Google Scholar secret is no longer used.

At build time, the website renders the complete checked-in snapshot through `_includes/inspire_publications.html`. In the browser it attempts to refresh from the `inspire-stats` feed, using the configured repository name. If the feed has not been published yet, is unavailable, or fails validation, the snapshot remains visible. Updating this feed does not depend on a GitHub Pages rebuild; visitors without JavaScript see the snapshot from the most recent website build.

## CV synchronization

During CV maintenance, refresh or read this same snapshot and compare shared paper facts using INSPIRE record ID, arXiv or DOI. Keep manual author-contribution groupings, translations and in-progress work in the CV source. The daily website workflow does not rewrite either CV repository or infer those editorial decisions. INSPIRE may omit non-HEP work or unpublished drafts; do not delete user-confirmed work merely because it is absent there.

Changes to papers displayed by the CV must be applied to both language versions and the relevant industry descriptions, followed by compilation and the website CV PDF synchronization specified in `AGENTS.md`.
