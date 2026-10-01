import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import main


def hit(identifier='1', author='1935435', title='Test paper', date='2025-01-01'):
    return {'id': identifier, 'metadata': {
        'titles': [{'title': title}], 'authors': [{'full_name': 'He, Jinchen', 'record': {'$ref': main.API + 'authors/' + author}}],
        'earliest_date': date, 'citation_count': 0,
    }}


AUTHOR = {'metadata': {'ids': [{'schema': 'INSPIRE BAI', 'value': 'Jinchen.He.1'}], 'name': {'value': 'He, Jinchen'}}}


class CrawlerTests(unittest.TestCase):
    def test_pagination_uses_unique_author_identifier(self):
        urls = []
        responses = iter([AUTHOR, {'hits': {'total': 2, 'hits': [hit()]}, 'links': {'next': main.API + 'literature?page=2'}},
                          {'hits': {'total': 2, 'hits': [hit('2', date='2026-01-01')]}}])
        def fetch(url):
            urls.append(url)
            return next(responses)
        data = main.collect('1935435', 1, fetch)
        self.assertIn('Jinchen.He.1', urls[1])
        self.assertEqual([p['id'] for p in data['publications']], ['2', '1'])

    def test_rejects_incomplete_duplicate_and_empty_results(self):
        for entries, total in [([hit()], 2), ([hit(), hit()], 2), ([], 0)]:
            responses = iter([AUTHOR, {'hits': {'total': total, 'hits': entries}}])
            with self.assertRaises(ValueError):
                main.collect('1935435', fetch=lambda _: next(responses))

    def test_rejects_wrong_author(self):
        with self.assertRaises(ValueError):
            main.normalize(hit(author='999'), '1935435')

    def test_title_math_and_html_are_safe(self):
        paper = main.normalize(hit(title='<math><msub><mi>g</mi><mi>A</mi></msub></math> & <b>TMD</b>'), '1935435')
        self.assertEqual(paper['title'], 'gA & TMD')
        html = main.render_html({'publications': [paper]}, {})
        self.assertIn('gA &amp; TMD', html)
        self.assertNotIn('<math>', html)
        self.assertIn('INSPIRE citations: 0', html)
        self.assertNotIn('INSPIRE citations:', main.render_html({'publications': [{**paper, 'citations': None}]}, {}))

    def test_preserves_personal_links_and_highlights_author_in_large_collaboration(self):
        paper = main.normalize(hit(), '1935435')
        paper['authors'] = [{'name': 'Other', 'self': False}] * 12 + [{'name': 'He, Jinchen', 'self': True}]
        html = main.render_html({'publications': [paper]}, {'1': {'links': [{'url': '/notes/poster.pdf', 'label': 'Poster'}]}})
        self.assertIn('<strong>Jinchen He</strong>', html)
        self.assertIn('et al.', html)
        self.assertIn('href="/notes/poster.pdf"', html)
        with self.assertRaises(ValueError):
            main.link('javascript:alert(1)', 'unsafe')

    def test_rate_limit_is_retried(self):
        error = HTTPError(main.API, 429, 'rate limited', {'Retry-After': '5'}, None)
        with patch.object(main, 'urlopen', side_effect=[error, error, error, error]), patch.object(main.time, 'sleep') as sleep:
            with self.assertRaises(HTTPError):
                main.fetch_json(main.API + 'authors/1935435')
            self.assertEqual(sleep.call_count, 3)
        with self.assertRaises(ValueError):
            main.fetch_json('https://example.com/api')

    def test_failed_fetch_does_not_overwrite_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'snapshot.json'
            main.write_snapshot({'old': True}, output)
            with patch.object(main, 'collect', side_effect=ValueError('Incomplete bibliography')), patch('sys.argv', ['main', '--output', str(output)]):
                with self.assertRaises(ValueError):
                    main.main()
            self.assertEqual(json.loads(output.read_text()), {'old': True})


if __name__ == '__main__':
    unittest.main()
