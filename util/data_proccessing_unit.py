import re
import requests
from bs4 import BeautifulSoup
import nagisa
import simplejson

def has_latin_characters(element):
    return bool(re.search('[a-zA-Z0-9]', element))

def delete_latin_words_from_list(list):
    return_list = []
    for sublist in list:
        new_sublist = [word for word in sublist if not has_latin_characters(word)]
        return_list.append(new_sublist)
    return return_list

def delete_newline_elements(word_list):
    return [sublist for sublist in word_list if not any('\n' in str(item) for item in sublist)]

def scrape_japanese_words(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        text_content = soup.get_text()

        words = nagisa.tagging(text_content).words
        tags = nagisa.tagging(text_content).postags
        word_tag_array = [[word, tag] for word, tag in zip(words, tags)]
        strings_to_delete = ['補助記号','空白','助詞','助動詞', '接尾辞']
        filtered_words = [element for element in word_tag_array if not any(e in element for e in strings_to_delete)]
        filtered_words = delete_latin_words_from_list(filtered_words)
        filtered_words = delete_newline_elements(filtered_words)
        return filtered_words

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
def translate_japanese_word(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            first_entry = data['data'][0]
            english_meanings = first_entry['senses'][0]['english_definitions']
            print(english_meanings)
        else:
            return "No translation found."
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return "Error fetching translation."