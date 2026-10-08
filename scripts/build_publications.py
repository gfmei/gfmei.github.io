"""Render the static publication list from the reviewed Scholar records."""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/data/publications.json').read_text())
papers = data['papers']
page = ROOT / 'publications/index.html'
text = page.read_text()
labels = {'conference': 'Conference paper', 'journal': 'Journal article', 'preprint': 'Preprint', 'manuscript': 'Manuscript'}
icons = {'PDF': 'far fa-file-pdf', 'Project': 'fas fa-external-link-alt', 'Code': 'fas fa-code', 'Google Scholar': 'fas fa-graduation-cap', 'Supplementary': 'far fa-file-alt', 'OpenReview': 'far fa-file-alt'}
years = sorted({p['year'] for p in papers if p['year']}, reverse=True)
counts = Counter(p['type'] for p in papers)

def esc(value):
    return html.escape(str(value), quote=True)

def venue_badge(paper):
    if paper['type'] == 'preprint': return 'arXiv'
    if paper['type'] != 'journal': return paper['venue']
    names = {'International Journal of Computer Vision': 'IJCV', 'Robotics and Automation Letters': 'RA-L', 'Network Science and Engineering': 'TNSE', 'Computational Social Systems': 'TCSS', 'Circuits and Systems I': 'TCSI', 'cybernetics': 'TCYB', 'Computer Vision and Image Understanding': 'CVIU', 'Neurocomputing': 'Neurocomputing', 'Algorithms': 'Algorithms', 'Complexity': 'Complexity', 'Scientific reports': 'Scientific Reports', 'Journal of Geology': 'Journal of Geology'}
    for name, badge in names.items():
        if name.lower() in paper['venue'].lower(): return badge
    return 'Journal'

def author_line(paper):
    names = []
    for index, author in enumerate(paper['authors']):
        own = bool(re.fullmatch(r'G\s+Mei', author, re.I))
        name = 'Guofeng Mei' if own else author
        value = esc(name)
        if index in paper.get('equal_contributors', []): value += '<sup>†</sup>'
        if index in paper.get('corresponding_authors', []): value += '<sup>*</sup>'
        names.append('<strong>' + value + '</strong>' if own else value)
    return ', '.join(names)

sections = []
number = 0
for year in years + ['undated']:
    group = [p for p in papers if (p['year'] or 'undated') == year]
    if not group: continue
    cards = []
    for p in group:
        number += 1
        family = 'neurips' if 'NeurIPS' in p['venue'] else 'cvpr' if 'CVPR' in p['venue'] else 'aaai' if 'AAAI' in p['venue'] else 'preprint' if p['type'] in ['preprint', 'manuscript'] else 'other'
        links = '\n'.join(f'                <a href="{esc(link["url"])}" target="_blank" rel="external nofollow noopener"><i class="{icons[link["label"]]}" aria-hidden="true"></i> {esc(link["label"])}</a>' for link in p['links'])
        cards.append(f'''            <li class="paper-card" data-venue="{family}" data-type="{p['type']}" id="{esc(p['id'])}" data-year="{year}">
              <span class="paper-number" aria-hidden="true">{number:02d}</span>
              <div class="paper-meta"><span class="venue-badge">{esc(venue_badge(p))}</span><span class="paper-type">{labels[p['type']]}</span>{'<span>'+year+'</span>' if year!='undated' else ''}</div>
              <h3>{esc(p['title'])}</h3>
              <p class="paper-authors">{author_line(p)}</p>
              <p class="paper-venue">{esc(p['venue'])}{', '+year if year!='undated' else ''}</p>
              <div class="paper-links">
{links}
              </div>
            </li>''')
    heading = 'Manuscripts' if year == 'undated' else year
    sections.append(f'''        <section class="publication-year" aria-labelledby="year-{year}">
          <div class="year-heading"><h2 id="year-{year}">{heading}</h2><span>{len(group)} {'work' if len(group)==1 else 'works'}</span></div>
          <ol class="paper-list">
{chr(10).join(cards)}
          </ol>
        </section>''')
# Keep the illustration and introduction while replacing the generated list and controls.
start = text.index('      <div class="publication-overview">')
end = text.index('    </main>', start)
nav = ''.join(f'<a href="#year-{y}">{y} <span>{sum(p["year"]==y for p in papers):02d}</span></a>' for y in years[:3])
if len(years)>3: nav += f'<a href="#year-{years[3]}">Earlier <span aria-hidden="true">↓</span></a>'
options = ''.join(f'<option value="{y}">{y}</option>' for y in years) + '<option value="undated">Undated manuscripts</option>'
types = ''.join(f'<option value="{kind}">{labels[kind]}s ({counts[kind]})</option>' for kind in labels)
content = f'''      <div class="publication-overview">
        <p><strong>{len(papers)}</strong> research works <span class="overview-divider" aria-hidden="true">/</span> <span>{years[-1]}–{years[0]}</span></p>
        <nav class="publication-year-nav" aria-label="Browse publications by year">{nav}</nav>
      </div>
      <p class="publication-contributions"><sup>†</sup> Equal contribution <span aria-hidden="true">·</span> <sup>*</sup> Corresponding author</p>
      <div class="publication-controls" hidden>
        <div class="publication-search"><label for="paper-search">Search publications</label><input id="paper-search" type="search" placeholder="Title, author, or venue…"></div>
        <div class="publication-filter"><label for="paper-year">Year</label><select id="paper-year"><option value="all">All years</option>{options}</select></div>
        <div class="publication-filter publication-type-filter"><label for="paper-type">Work type</label><select id="paper-type"><option value="all">All types</option>{types}</select></div>
      </div>
      <p id="publication-count" class="publication-count" role="status" aria-live="polite">{len(papers)} research works</p>
      <div id="publication-results">
{chr(10).join(sections)}
      </div>
      <p id="publication-empty" hidden>No publications match your search. Try another title, author, or venue.</p>
      <p class="publication-source-note">Updated from <a href="{esc(data['source_url'])}" target="_blank" rel="external nofollow noopener">Google Scholar</a> on October 8, 2026. Conference papers use the conference year; journal articles and preprints use the year recorded on Scholar.</p>
'''
text = text[:start] + content + text[end:]
text = text.replace('<h1>Selected <span>Publications</span></h1>', '<h1>Research <span>Publications</span></h1>')
text = text.replace('Selected publications by Guofeng Mei', 'Publications and preprints by Guofeng Mei')
page.write_text(text)
print(f'Rendered {len(papers)} research works.')
