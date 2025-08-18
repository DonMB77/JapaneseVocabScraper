import requests
from bs4 import BeautifulSoup
import nagisa
import util.data_proccessing_unit as dpu

def scrape_japanese_words(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        text_content = soup.get_text()

        words = nagisa.tagging(text_content).words
        tags = nagisa.tagging(text_content).postags
        word_tag_array = [[word, tag] for word, tag in zip(words, tags)]
        strings_to_delete = ['補助記号','空白','助詞','助動詞']
        filtered_words = [element for element in word_tag_array if not any(e in element for e in strings_to_delete)]
        filtered_words = dpu.delete_latin_words_from_list(filtered_words)

        print(filtered_words)
        return words

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":

    user_input_url = input("Please input an URL:  ")

    japanese_words = scrape_japanese_words(user_input_url)