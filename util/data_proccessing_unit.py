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
        strings_to_delete = ['補助記号','空白','助詞','助動詞', '接尾辞', '英単語']
        filtered_words = [element for element in word_tag_array if not any(e in element for e in strings_to_delete)]
        filtered_words = delete_latin_words_from_list(filtered_words)
        filtered_words = delete_newline_elements(filtered_words)
        filtered_words = [sublist for sublist in filtered_words if len(sublist) == 2]
        
        seen = set()
        unique_filtered_words = []
        for sublist in filtered_words:
            key = sublist[0]
            if key not in seen:
                unique_filtered_words.append(sublist)
                seen.add(key)
        return unique_filtered_words

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
def get_jisho_translation(word: str) -> dict:
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['data']:
            first_result = data['data'][0]
            all_translations = []
            for sense in first_result['senses']:
                all_translations.extend(sense['english_definitions'])
            furigana = ""
            if first_result['japanese']:
                furigana = first_result['japanese'][0].get('reading', "")
            return {
                "translations": all_translations,
                "furigana": furigana
            }
    except requests.exceptions.RequestException as e:
        return {"translations": ["Error fetching translation."], "furigana": ""}
        
    return {"translations": [], "furigana": ""}