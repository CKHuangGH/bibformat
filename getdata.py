import re
import requests
import time
checknamelist=[]

def format_ieee_title(title):
    lowercase_words = {
        "the", "for", "and", "nor", "but", "or", "yet", "so", "at", "around", "by",
        "after", "along", "from", "of", "on", "to", "with", "without", "in"
    }

    def capitalize_word(word):
        # Specific words and their required formats
        exceptions = {
            "iot": "IoT",
            "ieee": "IEEE",
            "openfog": "OpenFog",
            "kfiml": "KFIML",
            "slate": "SLATE",
            "cncf": "CNCF",
            "ec2": "EC2",
            "aws": "AWS",
            "ai": "AI",
            "5g": "5G",
            "devops": "DevOps",
            "api": "API",
            "Kubefed":"KubeFed"
        }
        if word.lower() in exceptions:
            return exceptions[word.lower()]
        return word.capitalize()

    words = re.split(r'(\W+)', title)
    # Handle the single-word case without duplication
    if len(words) == 1:
        return capitalize_word(words[0])
    
    formatted_words = [capitalize_word(words[0])]  # Always capitalize the first word

    # Track whether the previous token was a colon

    for word in words[1:]:
        if word.strip() and (word.strip().lower() not in lowercase_words):
            formatted_words.append(capitalize_word(word))
        else:
            formatted_words.append(word.lower())

    # Join the words back into a single string
    formatted_title = "".join(formatted_words).strip()

    return formatted_title

def remove_all_spaces(text):
  return re.sub(r"\s+", "", text)

def extract_middle_text(text):
  patterns = [r"\{\{(.+)\}\}", r"\{(.+)\}"]  # Patterns for double curly braces and curly braces
  for pattern in patterns:
    match = re.search(pattern, text)
    if match:
      return match.group(1)  # Return the extracted middle text
  return ""  # No match found

def add_double_brackets(text):
    def remove_commas(text):
        return re.sub(r"[,\n]", "", text)
    nocommas=remove_commas(text)
    middletext=extract_middle_text(nocommas)
    middletext=middletext.replace("{", "").replace("}", "")
    return middletext

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

with open('bib copy.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line[0]=='@':
            flagforscholar=0
            parts1 = line.split("@")
            parts2 = parts1[1].split("{")
            if parts2[0].lower()!="misc":
                flagforscholar=1
                print(parts2[0])
        if line[0]!='@' and flagforscholar==1:
            parts = line.split("=")
            entry=remove_all_spaces(parts[0])
            if entry=="title":
                #print(parts[1])
                titlename=add_double_brackets(parts[1])
                print(titlename)
                doi = search_crossref_by_title(titlename)
                if doi:
                    bibtex = get_bibtex_from_doi(doi)
                    with open('publication_bibtex.bib', 'a', encoding='utf-8') as file:
                        file.write(bibtex)
                    time.sleep(3)
                else:
                    print("No results found for the title.")


