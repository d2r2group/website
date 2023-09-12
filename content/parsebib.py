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

display(HTML("<ol>\n"))

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
    doi = bib_data.entries[e].fields['doi']
    dois.append(doi)

    # URLs
    url = bib_data.entries[e].fields['url']
    urls.append(url)

    # Comment
    if 'comment' in bib_data.entries[e].fields:
        if 'github.com' in bib_data.entries[e].fields['comment']:
            # add button
            pass

    display(HTML("<li>" + '\n' + name_string + "</li>"))

display(HTML('<ol>\n'))
# print(names_strings)
# print(years)
# print(journals)
# print(pages)
# print(vol_issue)
# print(dois)
# print(urls)
