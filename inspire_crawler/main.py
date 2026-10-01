"""Fetch this author's complete INSPIRE bibliography; no third-party dependencies."""
import argparse
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = 'https://inspirehep.net/api/'


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_title(value):
    parser = PlainText()
    parser.feed(value)
    return ''.join(parser.parts).strip()


def fetch_json(url):
    if urlsplit(url).hostname != 'inspirehep.net' or urlsplit(url).scheme != 'https':
        raise ValueError('Unexpected API pagination URL')
    for attempt in range(4):
        try:
            request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Jinchen-CV-Website/1.0'})
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code != 429 and error.code < 500:
                raise
            if attempt == 3:
                raise
            time.sleep(max(5, min(int(error.headers.get('Retry-After', '5')), 60)))
        except (URLError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))


def author_matches(author, author_id):
    ref = author.get('record', {}).get('$ref', '').rstrip('/')
    return ref.endswith('/authors/' + str(author_id)) or str(author.get('recid', '')) == str(author_id)


def normalize(hit, author_id):
    m = hit['metadata']
    authors = [{'name': a['full_name'], 'self': author_matches(a, author_id)} for a in m.get('authors', [])]
    if not any(a['self'] for a in authors):
        raise ValueError(f"Record {hit['id']} is not linked to the configured author")
    arxiv = list(dict.fromkeys(e['value'] for e in m.get('arxiv_eprints', [])))
    dois = list(dict.fromkeys(d['value'] for d in m.get('dois', [])))
    return {
        'id': str(hit['id']), 'title': plain_title(m['titles'][0]['title']),
        'authors': authors, 'arxiv': arxiv, 'dois': dois,
        'date': m.get('earliest_date') or m.get('preprint_date', ''),
        'publication_info': m.get('publication_info', []),
        'collaborations': [c['value'] for c in m.get('collaborations', [])],
        'citations': m.get('citation_count'),
        'url': 'https://inspirehep.net/literature/' + str(hit['id']),
    }


def collect(author_id, page_size=100, fetch=fetch_json):
    author = fetch(API + 'authors/' + str(author_id))
    bai = next(item['value'] for item in author['metadata']['ids'] if item['schema'] == 'INSPIRE BAI')
    url = API + 'literature?' + urlencode({'q': 'a ' + bai, 'size': page_size, 'sort': 'mostrecent'})
    query_url = url
    records, seen_urls, seen_ids = [], set(), set()
    total = None
    while url:
        if url in seen_urls:
            raise ValueError('Repeated pagination URL')
        seen_urls.add(url)
        page = fetch(url)
        count = page['hits']['total']
        count = count['value'] if isinstance(count, dict) else count
        if total is None:
            total = count
        elif total != count:
            raise ValueError('Bibliography changed during pagination; retry later')
        for hit in page['hits']['hits']:
            identifier = str(hit['id'])
            if identifier in seen_ids:
                raise ValueError('Duplicate record across API pages')
            seen_ids.add(identifier)
            records.append(normalize(hit, author_id))
        url = page.get('links', {}).get('next')
    if not records or len(records) != total:
        raise ValueError(f'Incomplete bibliography: received {len(records)} of {total}; preserving previous output')
    records.sort(key=lambda paper: (paper['date'], paper['id']), reverse=True)
    return {'author_id': str(author_id), 'author_name': author['metadata']['name'].get('preferred_name', author['metadata']['name']['value']),
            'author_bai': bai, 'source_url': query_url, 'publications': records}


def link(url, label):
    if urlsplit(url).scheme not in ('https', '') or (not urlsplit(url).scheme and not url.startswith('/')):
        raise ValueError('Unsafe publication link')
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def journal_label(info):
    journal = info.get('journal_title', '')
    if not journal:
        return ''
    volume = info.get('journal_volume', '')
    year = info.get('year', '')
    page = info.get('artid') or info.get('page_start', '')
    return ' '.join(str(part) for part in (journal, volume, f'({year})' if year else '', page) if part)


def render_html(data, extras):
    rows = []
    for paper in data['publications']:
        names = paper['authors']
        # Always retain the author's name, even in very large collaborations.
        shown = names[:10]
        if not any(a['self'] for a in shown):
            shown.append(next(a for a in names if a['self']))
        def display_name(author):
            last, separator, first = author['name'].partition(', ')
            return escape(first + ' ' + last if separator else last)
        authors = ', '.join(f'<strong>{display_name(a)}</strong>' if a['self'] else display_name(a) for a in shown)
        if len(names) > len(shown):
            authors += ', et al.'
        parts = [link(paper['url'], paper['title']), authors.rstrip('.')]
        parts.extend(escape(c) for c in paper['collaborations'])
        journals = [journal_label(info) for info in paper['publication_info']]
        parts.extend(escape(j) for j in dict.fromkeys(journals) if j)
        parts.extend(link('https://arxiv.org/abs/' + a, 'arXiv:' + a) for a in paper['arxiv'])
        parts.extend(link('https://doi.org/' + d, 'DOI') for d in paper['dois'])
        if paper['citations'] is not None:
            parts.append(f'INSPIRE citations: {int(paper["citations"])}')
        extra = extras.get(paper['id'], {})
        parts.extend(link(item['url'], item['label']) for item in extra.get('links', []))
        rows.append(f'<li data-inspire-id="{paper["id"]}">' + '. '.join(parts) + '.</li>')
    return '<ul class="inspire-publications">\n' + '\n'.join(rows) + '\n</ul>'


def write_snapshot(data, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    # A failed/incomplete fetch never reaches this atomic replacement.
    temp = output.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    os.replace(temp, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_data/inspire_publications.json')
    parser.add_argument('--page-size', type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.page_size <= 1000:
        parser.error('page size must be between 1 and 1000')
    config = json.loads((ROOT / '_data/inspire_config.json').read_text())
    author_id = config['author_id']
    data = collect(author_id, args.page_size)
    extras = json.loads((ROOT / '_data/publication_extras.json').read_text())
    data['html'] = render_html(data, extras)
    citations = [p['citations'] for p in data['publications']]
    data['total_citations'] = sum(citations) if all(c is not None for c in citations) else None
    data['updated'] = datetime.now(timezone.utc).isoformat()
    data['schema_version'] = 1
    write_snapshot(data, args.output)
    print(f"Fetched {len(data['publications'])} publications for {data['author_name']} ({data['author_bai']})")


if __name__ == '__main__':
    main()
