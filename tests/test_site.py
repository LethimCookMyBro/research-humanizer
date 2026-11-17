"""Local website contracts; these do not establish search engine indexing."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
BASE = 'https://research-humanizer.vercel.app'
PAGES = {'index.html': ('en', BASE + '/'), 'th/index.html': ('th', BASE + '/th/')}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
    def select(self, tag):
        return [a for t, a in self.elements if t == tag]

class SiteTests(unittest.TestCase):
    def read(self, rel):
        p = SITE / rel
        self.assertTrue(p.is_file(), f'Missing site file {rel}')
        return p.read_text(encoding='utf-8')
    def test_languages_titles_descriptions(self):
        descriptions = []
        for rel, (lang, _) in PAGES.items():
            text = self.read(rel)
            p = Page(text)
            self.assertEqual(p.select('html')[0]['lang'], lang)
            self.assertEqual(len(p.select('h1')), 1)
            self.assertEqual(len(p.select('title')), 1)
            self.assertIn('Research Humanizer', text.split('<title>')[1].split('</title>')[0])
            meta = {m.get('name'): m.get('content') for m in p.select('meta')}
            self.assertTrue(50 <= len(meta['description']) <= 250)
            self.assertNotIn('noindex', meta.get('robots', ''))
            self.assertIn('viewport', meta)
            descriptions.append(meta['description'])
        self.assertNotEqual(*descriptions)
    def test_canonical_and_reciprocal_alternates(self):
        for rel, (_, canonical) in PAGES.items():
            p = Page(self.read(rel))
            self.assertEqual([a['href'] for a in p.select('link') if a.get('rel') == 'canonical'], [canonical])
            alternates = {a['hreflang']: a['href'] for a in p.select('link') if a.get('rel') == 'alternate'}
            self.assertEqual(alternates, {'en': BASE+'/', 'th': BASE+'/th/', 'x-default': BASE+'/'})
    def test_social_metadata(self):
        for rel, (_, canonical) in PAGES.items():
            p = Page(self.read(rel))
            meta = {a.get('property'): a.get('content') for a in p.select('meta')}
            self.assertEqual(meta['og:url'], canonical)
            self.assertIn('Research Humanizer', meta['og:title'])
            self.assertTrue(meta['og:description'])
    def test_schema_has_true_identity_no_fake_ratings(self):
        for rel in PAGES:
            text = self.read(rel)
            raw = text.split('<script type="application/ld+json">')[1].split('</script>')[0]
            data = json.loads(raw)
            self.assertEqual(data['@type'], 'SoftwareSourceCode')
            self.assertEqual(data['codeRepository'], 'https://github.com/LethimCookMyBro/research-humanizer')
            self.assertEqual(data['softwareVersion'], (ROOT/'VERSION').read_text().strip())
            self.assertNotIn('aggregateRating', data)
            self.assertNotIn('review', data)
    def test_static_content_commands_and_limits(self):
        for rel in PAGES:
            text = self.read(rel)
            for command in ('/plugin marketplace add LethimCookMyBro/research-humanizer', '/plugin install research-humanizer@research-humanizer', '/research-humanizer:research-full'):
                self.assertIn(command, text)
            self.assertIn('CC BY-NC 4.0', text)
            self.assertIn('Preview', text)
            self.assertIn('docs/VERIFICATION.md', text)
            self.assertNotIn('<form', text)
    def test_local_links_and_fragments(self):
        for rel in (*PAGES, '404.html'):
            text = self.read(rel)
            p = Page(text)
            ids = [a['id'] for _, a in p.elements if 'id' in a]
            self.assertEqual(len(ids),len(set(ids)))
            for tag, a in p.elements:
                target = a.get('href') or a.get('src')
                if not target or urlsplit(target).scheme:
                    continue
                u = urlsplit(target)
                path = SITE / unquote(u.path).lstrip('/') if u.path.startswith('/') else SITE / Path(rel).parent / unquote(u.path)
                if not u.path:
                    path = SITE / rel
                if path.is_dir():
                    path /= 'index.html'
                self.assertTrue(path.is_file(), str(path))
                if u.fragment:
                    target_ids = [a['id'] for _,a in Page(path.read_text()).elements if 'id' in a]
                    self.assertIn(u.fragment,target_ids)
    def test_sitemap_and_robots(self):
        text = self.read('sitemap.xml')
        root = ET.fromstring(text)
        urls = [e.text for e in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(set(urls), {BASE+'/', BASE+'/th/'})
        robots = self.read('robots.txt')
        self.assertIn('Sitemap: '+BASE+'/sitemap.xml', robots)
        self.assertNotIn('Disallow: /', robots)
    def test_no_external_runtime_tracking_dependencies(self):
        for rel in PAGES:
            p = Page(self.read(rel))
            for script in p.select('script'):
                if script.get('src'):
                    self.assertTrue(script['src'].startswith('/'))
            self.assertLess((SITE/rel).stat().st_size, 40000)
        self.assertLess((SITE/'styles.css').stat().st_size, 20000)
    def test_404_not_indexable(self):
        p = Page(self.read('404.html'))
        self.assertIn('noindex', next(a['content'] for a in p.select('meta') if a.get('name') == 'robots'))
    def test_readmes_point_to_public_site(self):
        for rel in ('README.md','README(TH).md'):
            self.assertIn(BASE, (ROOT/rel).read_text())

if __name__ == '__main__':
    unittest.main()
