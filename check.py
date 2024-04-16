import re

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
    def writesametitle(text):
        with open("sametitle.txt", "a", encoding='utf-8') as f:
            f.write(text+"\n")
    def remove_commas(text):
        return re.sub(r"[,\n]", "", text)
    nocommas=remove_commas(text)
    middletext=extract_middle_text(nocommas)
    middletext=middletext.replace("{", "").replace("}", "")
    ieeetext=format_ieee_title(middletext.lower())
    
    if '\'S' in ieeetext:
        ieeetext=ieeetext.replace("'S", "'s")
    
    if ieeetext not in checknamelist:
        checknamelist.append(ieeetext)
    else:
        writesametitle(ieeetext)
    return "{{" + ieeetext+ "}}"+","+"\n"
        
def writebib(text):
    with open("biblio.bib", "a", encoding='utf-8') as f:
        f.write(text)


with open('bib.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # if line[0]=='@':
        #    writebib(line.lower())
        if line[0]!='@':
            parts = line.split("=")
            entry=remove_all_spaces(parts[0])
            if entry=="title":
                titlename=add_double_brackets(parts[1])
                print(titlename)
                # writebib(titlename)
            # with open("biblio.bib", "a", encoding='utf-8') as f:
            #     f.write(line.lstrip())