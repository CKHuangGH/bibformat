import requests

def search_crossref_by_title(title):
    """Search for a paper by title on Crossref and return DOI."""
    params = {
        'query.title': title,
        'rows': 1,  # fetch only the first result
        'select': 'DOI,title'  # return only DOI and title
    }
    response = requests.get('https://api.crossref.org/works', params=params)
    if response.status_code == 200:
        results = response.json()
        if results['message']['items']:
            return results['message']['items'][0]['DOI']
    return None

def get_bibtex_from_doi(doi):
    """Fetch BibTeX citation for a given DOI."""
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "BibTeX not found or error in fetching."

# Example title search
title = "Computing Without Borders: The Way Towards Liquid Computing"
doi = search_crossref_by_title(title)
if doi:
    bibtex = get_bibtex_from_doi(doi)
    print(bibtex)
else:
    print("No results found for the title.")