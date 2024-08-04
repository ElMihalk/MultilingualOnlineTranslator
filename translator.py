import bs4
import requests
from bs4 import BeautifulSoup
import re
import sys


LANGUAGES = {
    1: "Arabic",
    2: "German",
    3: "English",
    4: "Spanish",
    5: "French",
    6: "Hebrew",
    7: "Japanese",
    8: "Dutch",
    9: "Polish",
    10: "Portuguese",
    11: "Romanian",
    12: "Russian",
    13: "Turkish"
}

#inverted dictionary
NUMBERS_FROM_LANGUAGES = {v: k for k, v in LANGUAGES.items()}
NUMBERS_FROM_LANGUAGES.update({"All": 0})

_, language_from, language_to, word = sys.argv

if language_from.capitalize() not in NUMBERS_FROM_LANGUAGES.keys():
    print(f"Sorry, the program doesn't support {language_from}")
    sys.exit()
elif language_to.capitalize() not in NUMBERS_FROM_LANGUAGES.keys():
    print(f"Sorry, the program doesn't support {language_to}")
    sys.exit()
else:
    language_from = NUMBERS_FROM_LANGUAGES[language_from.capitalize()]
    language_to = NUMBERS_FROM_LANGUAGES[language_to.capitalize()]

def find_literal_translations(source: bs4.BeautifulSoup):
    literal_translations = []
    term_lines = source.find_all(name="span", class_="display-term")
    for line in term_lines:
        literal_translations.append(line.get_text())

    return literal_translations

def find_context_translations(source: bs4.BeautifulSoup):
    context_translations = []
    term_lines = source.find_all(name="span", attrs={"class": "text"})
    context_translations = [line.get_text().lstrip() for line in term_lines if re.match(r"^\s", line.get_text())]

    return context_translations

def output_results(language_to: int, source: bs4.BeautifulSoup, word: str):
    global LANGUAGES

    with open(f"{word}.txt", "a", encoding="utf-8") as f:
        print()
        print(f"{LANGUAGES[language_to]} Translations")
        f.write(f"{LANGUAGES[language_to]} Translations")
        f.write("\n")
        translations = find_literal_translations(source=source)
        print(translations[0])
        f.write(translations[0])
        f.write("\n")

        examples = find_context_translations(source=source)
        print()
        f.write("\n")
        print(f"{LANGUAGES[language_to]} Examples")
        f.write(f"{LANGUAGES[language_to]} Examples")
        f.write("\n")
        print(examples[0])
        f.write(examples[0])
        f.write("\n")
        print(examples[1])
        f.write(examples[1])
        f.write("\n")
        f.write("\n")

# #introduction
# print("Hello, welcome to the translator. Translator supports:")
# for item in LANGUAGES:
#     print(f"{item}. {LANGUAGES[item]}")
#
# # language input
# language_from = int(input("Type the number of your language: "))
# language_to = int(input("Type the number of a language you want to translate to or '0' to translate to all languages: "))
#
# # word input
# word = input("Type the word you want to translate:")

#loop over languages
if language_to == 0:
    to_translate = list(LANGUAGES.keys())
    to_translate.remove(language_from)
else:
    to_translate = [language_to]

for item in to_translate:
    language_to = item
    #get page content
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(
            url=f"https://context.reverso.net/translation/{LANGUAGES[language_from].lower()}-{LANGUAGES[language_to].lower()}/{word}",
            headers=headers
        )
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()
    if response.status_code != 200:
        print(f"Sorry, unable to find {word}")
        sys.exit()
    soup = BeautifulSoup(response.text, "html.parser")

    #output results
    output_results(language_to=language_to, source=soup, word=word)
