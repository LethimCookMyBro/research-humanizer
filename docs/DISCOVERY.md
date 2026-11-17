# Discoverability and search setup

This is a website/documentation update. Research Humanizer stays at v2.3.0. Search visibility is not a product-quality benchmark, and neither indexing nor rankings are guaranteed.

## Public destinations

- English website `https://research-humanizer.vercel.app/`
- Thai website `https://research-humanizer.vercel.app/th/`
- Sitemap `https://research-humanizer.vercel.app/sitemap.xml`
- Source repository `https://github.com/LethimCookMyBro/research-humanizer`

The site source is `site/`. The linked Vercel project builds that directory as plain static files, with no installation or build command. Production is public; previews retain authentication. The website contains no forms, analytics, external fonts or manuscript uploads. The host used to run the skill has its own data policies.

## Implemented in source

The English and Thai pages have meaningful titles and descriptions, unique canonical URLs, reciprocal language alternates, semantic HTML, crawlable links, and SoftwareSourceCode structured data. The schema does not invent reviews, ratings, a DOI or provider endorsement. Installation and full-paper prompts are visible without needing JavaScript. JavaScript only enhances copying. The sitemap names the two public pages, and root robots.txt points to it.

Both repository READMEs link to the website and the versioned preview release. The existing skill, version, licenses and historical release assets are unchanged. No fake stars, keyword stuffing, paid backlinks, doorway pages or mass directory submissions are used.

## GitHub About fields to apply with administrator access

The available GitHub connector could update source files but did not expose repository administration. The following are prepared settings, not a claim that those fields were changed.

Open the repository and choose the gear beside About. Use this description.

```text
Research humanizer skill for full academic papers in Claude Code and Codex. Pair with ARS for source-bound prose, equations, graphs and Word checks. English + Thai.
```

Website

```text
https://research-humanizer.vercel.app/
```

Suggested Topics, entered individually

```text
research-humanizer
academic-writing
scientific-writing
research-writing
agent-skills
claude-code
codex
humanizer
research-integrity
reproducible-research
thai
```

These settings improve the repository's description and topic navigation. They do not control Google's ranking.

## Google Search Console

Only the owner or an authorized full user can request indexing. No connected verified Search Console property was available during this update, so no indexing request or sitemap submission is claimed.

1. Add the exact URL-prefix property `https://research-humanizer.vercel.app/` in Search Console. This is a project subdomain, not ownership of all of `vercel.app`.
2. Choose HTML-tag or HTML-file verification. Copy the actual Google-issued tag into both page heads, or place the exact verification file in `site/`, then publish. Do not invent a verification token. Keep it published after verification.
3. After ownership is verified, submit `sitemap.xml` in Sitemaps.
4. Inspect the English and Thai URLs, run the live test, and request indexing when eligible. Record the actual response. A successful request is not proof of indexing or ranking.
5. Monitor Page indexing and Performance for observed impressions, clicks and queries. Do not infer index coverage from a single broad search or from a `site:` query alone.

Do not use Google's Indexing API for these documentation pages. No bulk indexing service or obsolete sitemap-ping URL is part of this setup.

## Maintaining the public website

When the package changes, update the site's visible version, release links and structured-data version together. The website contracts check them against `VERSION`. Review the public text against the actual release and keep the Preview caveats until supported evidence changes.

Changing the canonical domain requires updating both pages, reciprocal alternate links, robots.txt, sitemap.xml, READMEs and tests. Keep one production canonical host. Do not leave indexable duplicates on multiple deployments. Never use an authentication-bypass URL as the canonical address.

Only share the public website and released examples. Ask before posting announcements to communities or submitting a listing under someone else's rules. Do not publish private research as a demonstration.

## Validation

Local suites after this change pass 60 repository tests, 134 skill tests and 5 historical regressions. The 10 new site contracts failed before the website existed. They check metadata, language links, local file targets, sitemap, public indexing directives, release identity and visible commands.

Offline Chromium previews were checked at 1440, 390 and 320 pixels for both languages. Copy-handler tests used a mocked clipboard. Expandable sections and horizontal overflow were checked. This is not a Google crawl or a live operating-system clipboard test. Local HTTP navigation was blocked by browser policy; source HTML and CSS were rendered offline instead. Public deployment and response headers are checked separately after publishing.

## Official references

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Ask Google to recrawl URLs](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
- [Google crawling and indexing FAQ](https://developers.google.com/search/help/crawling-index-faq)
- [GitHub repository topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)

Reviewed on 17 November 2026. The site and source changes make the material accessible to readers and crawlers. They do not establish inclusion in any search engine.
