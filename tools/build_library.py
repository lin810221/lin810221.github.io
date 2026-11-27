"""Generate the offline course library from explicit organization + course catalogs."""
import argparse
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools/library.json'


def esc(value):
    return html.escape(str(value), quote=True)


def library_data():
    data = json.loads(SOURCE.read_text(encoding='utf-8'))
    domains = {d['id']: d for d in data['domains']}
    levels = {d['id']: d for d in data['levels']}
    catalogs = {p.parent.name: p for p in ROOT.glob('*/course.json')}
    if set(catalogs) != set(data['courses']):
        raise ValueError('Every course needs library metadata; missing: ' + str(sorted(set(catalogs)-set(data['courses']))) + '; stale: ' + str(sorted(set(data['courses'])-set(catalogs))))
    courses = []
    for slug, entry in data['courses'].items():
        catalog = json.loads(catalogs[slug].read_text(encoding='utf-8'))
        assert entry['domain'] in domains, slug
        assert entry['group'] in domains[entry['domain']]['groups'], slug
        assert entry['level'] in levels, slug
        assert entry['tags'] and len(entry['tags']) == len(set(entry['tags'])), slug
        assert all(tag in data['tags'] for tag in entry['tags']), slug
        assert (ROOT/'assets/course-icons'/f'{slug}.svg').is_file(), slug
        assert isinstance(entry.get('classicOrder'), int), slug
        assert all(isinstance(entry['classic'][k], str) for k in ('name','subtitle','eyebrow','description','action')), slug
        courses.append(dict(entry, slug=slug, href=f'{slug}/index.html', updated=catalog['updated'],
                            chapters=sum(str(g['number']).isdigit() for g in catalog['groups']),
                            units=[l['id'] for l in catalog['lessons']], fullTitle=catalog['title']))
    courses.sort(key=lambda c: (list(domains).index(c['domain']), domains[c['domain']]['groups'].index(c['group']), list(levels).index(c['level']), c['order']))
    data['courses'] = courses
    assert len({c['classicOrder'] for c in courses}) == len(courses), 'Classic course order must be unique'
    assert all(t in data['tags'] for t in data['featuredTags'])
    for route in data['routes']:
        assert route['domain'] in domains
        assert len(route['courses']) == len(set(route['courses']))
        assert all(slug in catalogs for slug in route['courses'])
    for key in ('domains', 'levels', 'routes'):
        ids = [x['id'] for x in data[key]]
        assert len(ids) == len(set(ids)), key
    return data


def tag_button(tag, data, count=None):
    label = data['tags'][tag]
    number = f'<span class="tag-count" data-tag-count="{tag}">{count}</span>' if count is not None else ''
    return f'<button type="button" class="tag" data-tag="{tag}" aria-pressed="false"><span class="sr-only">篩選標籤：</span><span>#{esc(label)}</span>{number}</button>'


def card(course, data):
    c = course
    level = next(x['title'] for x in data['levels'] if x['id'] == c['level'])
    tags = ''.join(tag_button(t, data) for t in c['tags'])
    # The original SVG artwork supplies each cover's color; its geometry stays intact.
    accent = ET.parse(ROOT/'assets/course-icons'/f'{c["slug"]}.svg').getroot().get('color', '#b5e99b')
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', accent):
        raise ValueError('Invalid course cover color: ' + c['slug'])
    classic = c['classic']
    styles = (ROOT/'assets/style.css').read_text(encoding='utf-8')
    classic_background = '#171e18'
    for cls in classic['artClasses']:
        if not re.fullmatch(r'[a-z-]+', cls):
            raise ValueError('Invalid classic artwork class')
        rule = re.search(r'\.'+re.escape(cls)+r'\{([^}]+)\}', styles)
        background = re.search(r'(?:^|;)background:([^;]+)', rule[1]) if rule else None
        if background:
            classic_background = background[1]
    classic_metrics = ''.join(f'<span>{esc(text)}</span>' for text in classic['extraMeta'])
    return f'''<article class="subject-feature course-card" data-course="{c['slug']}">
<a class="course-card-link" href="{c['href']}" aria-labelledby="title-{c['slug']}">
<div class="course-cover" style="--cover-accent:{accent};--classic-background:{esc(classic_background)}" aria-hidden="true"><img class="course-icon" src="assets/course-icons/{c['slug']}.svg" width="300" height="208" alt="" loading="lazy"><span class="cover-caption">{esc(c['coverCaption'])}</span></div>
<div class="subject-copy classic-copy"><span class="eyebrow">{esc(classic['eyebrow'])}<span>／ {c['classicOrder']:02d}</span></span><h2 id="classic-title-{c['slug']}">{esc(classic['name'])} <span>{esc(classic['subtitle'])}</span></h2><p>{esc(classic['description'])}</p><div class="subject-meta"><span>{c['chapters']} 章・{len(c['units'])} 個單元</span>{classic_metrics}</div><span class="text-link">{esc(classic['action'])} <span aria-hidden="true">↗</span></span></div>
<div class="course-card-copy">
<div class="course-card-kicker"><span class="level-badge level-{c['level']}"><span class="sr-only">建議起點：</span>{level}</span><span class="card-size">{c['chapters']} 章 <span aria-hidden="true">·</span> {len(c['units'])} 單元</span></div>
<h4 id="title-{c['slug']}">{esc(c['title'])}</h4>
<p class="card-description">{esc(c['description'])}</p>
<p class="prerequisite"><span>先備建議</span>{esc(c['prerequisite'])}</p>
<span class="card-open">開始閱讀<span aria-hidden="true">↗</span></span>
</div>
</a>
<div class="card-tags enhancement" hidden aria-label="{esc(c['title'])}的標籤">{tags}</div>
<div class="course-progress" hidden><span data-progress-label></span><progress max="{len(c['units'])}" value="0" aria-label="{esc(c['title'])}完成進度"></progress></div>
</article>'''


def outputs():
    data = library_data()
    courses = data['courses']
    domain_cards, sections = [], []
    for i, domain in enumerate(data['domains'], 1):
        subset = [c for c in courses if c['domain'] == domain['id']]
        domain_cards.append(f'''<a class="domain-entry" href="#domain-{domain['id']}" data-domain="{domain['id']}" data-domain-label="{esc(domain['title'])}">
<span class="domain-entry-top"><span class="domain-symbol" aria-hidden="true">{domain['symbol']}</span><span>{len(subset):02d} 門課程</span></span>
<h3>{domain['title']}<span aria-hidden="true">↗</span></h3><p>{domain['description']}</p><span class="domain-english">{domain['english']}</span></a>''')
        groups = []
        for group in domain['groups']:
            group_courses = [c for c in subset if c['group'] == group]
            groups.append(f'<section class="course-subgroup" data-course-group><h3 class="subgroup-title">{esc(group)}</h3><div class="course-grid">' + '\n'.join(card(c, data) for c in group_courses) + '</div></section>')
        sections.append(f'''<section class="domain-group" id="domain-{domain['id']}" data-domain-group="{domain['id']}" aria-labelledby="heading-{domain['id']}">
<div class="domain-heading"><span class="domain-symbol" aria-hidden="true">{domain['symbol']}</span><div><span class="domain-english">{domain['english']}</span><h2 id="heading-{domain['id']}">{domain['title']}</h2></div><span class="domain-result-count">{len(subset)} 門課程</span></div>
{''.join(groups)}</section>''')
    lookup = {c['slug']: c for c in courses}
    routes = []
    for route in data['routes']:
        route_steps = ''.join(f'<li>{esc(lookup[s]["title"])}</li>' for s in route['courses'])
        routes.append(f'''<article class="route-card"><h3>{esc(route['title'])}</h3><p>{esc(route['description'])}</p><ol class="route-steps">{route_steps}</ol><p class="route-note">{esc(route['note'])}</p><button class="route-select enhancement" hidden type="button" data-route="{route['id']}" aria-pressed="false">查看這條路線 <span aria-hidden="true">↗</span></button></article>''')
    levels = '<button type="button" class="filter-pill" data-level="all" aria-pressed="true">全部起點</button>' + ''.join(f'<button type="button" class="filter-pill" data-level="{l["id"]}" aria-pressed="false" title="{esc(l["description"])}">{l["title"]}</button>' for l in data['levels'])
    tags = lambda keys: ''.join(tag_button(t, data, sum(t in c['tags'] for c in courses)) for t in keys)
    recent = ''.join(f'<li><time datetime="{c["updated"]}">{c["updated"]}</time><a href="{c["href"]}#{c["units"][0]}">{esc(c["title"])}</a></li>' for c in sorted(courses, key=lambda c: (c['updated'], c['slug']), reverse=True)[:3])
    template = Template((ROOT/'tools/library-template.html').read_text(encoding='utf-8'))
    page = template.substitute(total=len(courses), domain_total=f'{len(data["domains"]):02d}', unit_total=f'{sum(len(c["units"]) for c in courses):,}',
        domain_cards='\n'.join(domain_cards), course_sections='\n'.join(sections), routes='\n'.join(routes),
        level_filters=levels, featured_tags=tags(data['featuredTags']),
        more_tags=tags([t for t in data['tags'] if t not in data['featuredTags']]), recent=recent)
    serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return {'index.html': page, 'assets/library-data.js': '/* Generated by tools/build_library.py; edit tools/library.json. */\nwindow.LEARNING_LIBRARY = ' + serialized + ';\n'}


def build_library(check=False):
    for relative, content in outputs().items():
        path = ROOT/relative
        if check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                raise ValueError(f'Stale library output: {relative}; run python tools/build_library.py')
        else:
            path.write_text(content, encoding='utf-8')
    print('Library: all courses organized; ' + ('generated files current' if check else 'HTML and offline data generated'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build_library(parser.parse_args().check)
