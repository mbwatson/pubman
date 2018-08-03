import requests

def fetchCitation(doi, citation_format='apa'):
    url = f'https://search.crossref.org/citation?format={citation_format}&doi={doi}'
    citation = requests.get(url)
    citation.encoding = 'utf-8'
    return citation.text or None

def buildAuthorListFor(publication):
    pass
