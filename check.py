import re


def format_ieee_title(title):
    # List of words to keep lowercase unless they are the first or last word
    lowercase_words = {
        "the", "for", "and", "nor", "but", "or", "yet", "so", "at", "around", "by",
        "after", "along", "for", "from", "of", "on", "to", "with", "without", "in"
    }

    # Function to capitalize words keeping specific exceptions
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
            "api": "API"
        }
        # Check for possessive 's
        if word.lower().endswith("'s"):
            base_word = word[:-2]
            if base_word.lower() in exceptions:
                return exceptions[base_word.lower()] + "'s"
            else:
                return base_word.capitalize() + "'s"
        elif word.lower() in exceptions:
            return exceptions[word.lower()]
        return word.capitalize()

    # Split title into words, taking into account punctuation like colons
    words = re.split(r'(\W+)', title)

    # Handle the single-word case without duplication
    if len(words) == 1:
        return capitalize_word(words[0])

    # Apply rules for each word in the title
    formatted_words = [
        capitalize_word(words[0])  # Always capitalize the first word
    ] + [
        capitalize_word(word) if word.lower().strip() not in lowercase_words and word not in ["'S", "'s"] else word.lower()
        for word in words[1:-1]  # Capitalize middle words based on rules
    ] + [
        capitalize_word(words[-1])  # Always capitalize the last word
    ]

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
    nobrackets=nocommas
    middletext=extract_middle_text(nobrackets)
    ieeetext=format_ieee_title(middletext.lower())
    finishtext=ieeetext.replace("{", "").replace("}", "")
    print(finishtext)
    return "{{" + finishtext+ "}}"+","+"\n"
        
def writebib(text):
    with open("biblio.bib", "a", encoding='utf-8') as f:
        f.write(text)


with open('bib.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line[0]=='@':
           writebib(line.lower())
        if line[0]!='@':
            parts = line.split("=")
            entry=remove_all_spaces(parts[0])
            if entry=="title":
                titlename=add_double_brackets(parts[1])
                writebib(titlename)
            # with open("biblio.bib", "a", encoding='utf-8') as f:
            #     f.write(line.lstrip())