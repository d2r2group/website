from pybtex.database.input import bibtex
from IPython.display import display, Markdown, HTML


def readable_list(author_list):
    if len(author_list) == 1:
        return str(author_list[0])
    elif len(author_list) < 3:
        return ' and '.join(map(str, author_list))
    *a, b = author_list
    return f"{', '.join(map(str, a))}, and {b}"


def button(url, label, icon):
    icon_base = icon[:2]
    return f"""<a class="btn btn-outline-dark btn-sm", href="{url}" target="_blank" rel="noopener noreferrer">
    <i class="{icon_base} {icon}" role='img' aria-label='{label}'></i> {label} </a>"""


parser = bibtex.Parser()
bib_data = parser.parse_file('biblio.bib')

names_strings = []
titles = []
years = []
journals = []
vol_issue = []
pages = []
dois = []
urls = []

entries = []

for e in bib_data.entries:
    # Names
    names = [' '.join([b[0] + '.' for b in a.first_names]) + ' ' + ' '.join([c[0] + '.' for c in a.middle_names]) +
             ' ' + ' '.join(a.last_names) for a in bib_data.entries[e].persons['author']]
    name_string = readable_list([n.replace('  ', ' ').replace('Â', '') for n in names])
    names_strings.append(name_string)

    # Title
    title = bib_data.entries[e].fields['title'].replace('{', '').replace('}', '')
    titles.append(title)

    # Year
    year = bib_data.entries[e].fields['year']
    years.append(year)

    # Volume and Issue
    vi = ''
    if 'volume' in bib_data.entries[e].fields:
        vi += bib_data.entries[e].fields['volume']
    if 'number' in bib_data.entries[e].fields:
        vi += ', ' + bib_data.entries[e].fields['number']

    # Pages
    page = bib_data.entries[e].fields['pages'] if 'pages' in bib_data.entries[e].fields else ''
    pages.append(page)

    # Journal
    if 'journal' in bib_data.entries[e].fields:
        journal = bib_data.entries[e].fields['journal'].replace('\\', '')
    elif 'arXiv' in bib_data.entries[e].fields['publisher']:
        journal = 'arXiv'
        vi = bib_data.entries[e].fields['note'].split(' ')[0]
    else:
        raise ValueError('Error. No journal or publisher specified.')

    journals.append(journal)
    vol_issue.append(vi)
    # print(bib_data.entries[e].fields.values())

    # DOI
    try:
        doi = bib_data.entries[e].fields['doi']
    except KeyError:
        doi = None
    dois.append(doi)

    # URLs
    url = bib_data.entries[e].fields['url'] if 'url' in bib_data.entries[e].fields else None
    urls.append(url)

    # Comment
    comment = bib_data.entries[e].fields['comment'] if 'comment' in bib_data.entries[e].fields else None

    entries.append({
        'name_string': name_string,
        'title': title,
        'year': year,
        'vi': vi,
        'page': page,
        'journal': journal,
        'doi': doi,
        'comment': comment,
    })

# Entries that only have a preprint (arXiv/chemRxiv) and no DOI yet are not peer-reviewed.
preprint_entries = [entry for entry in entries if entry['doi'] is None]
paper_entries = [entry for entry in entries if entry['doi'] is not None]

n_papers = len(paper_entries)
n_total = len(entries)


def render_entry(entry, value):
    html = f"<li value='{value}'>\n"
    html += f"<i>{entry['title']}</i><br>\n"
    html += f"<b>{entry['journal']} {entry['vi']} ({entry['year']})</b> {entry['page']}<br>\n"
    html += f"<small>{entry['name_string']}</small><br>\n"
    if entry['doi'] is not None:
        html += button('https://doi.org/' + entry['doi'], 'Published', 'ai-archive')
    if entry['comment']:
        for link in str(entry['comment']).split(';'):
            if 'arxiv.org' in link or 'chemrxiv' in link:
                html += ' ' + button(link, 'Preprint', 'bi-file-earmark-pdf')
            if 'github.com' in link:
                html += ' ' + button(link, 'GitHub', 'bi-github')
    html += "</li>"
    return html


display(Markdown('## Preprints'))

if preprint_entries:
    preprint_html = f'<ol style="counter-reset: num {n_total+1};list-style-type: none;">\n'
    for ind, entry in enumerate(preprint_entries):
        preprint_html += render_entry(entry, n_total - ind)
    preprint_html += "</ol>\n"
    display(HTML(preprint_html))
else:
    display(Markdown('Currently no preprints that have not been peer-reviewed.'))

display(Markdown('## Publications'))

paper_html = f'<ol style="counter-reset: num {n_papers+1};list-style-type: none;">\n'
for ind, entry in enumerate(paper_entries):
    paper_html += render_entry(entry, n_papers - ind)
paper_html += "</ol>\n"

display(HTML(paper_html))

# print(names_strings)
# print(years)
# print(journals)
# print(pages)
# print(vol_issue)
# print(dois)
# print(urls)
