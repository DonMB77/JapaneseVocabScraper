import requests
from bs4 import BeautifulSoup
import nagisa
import sys

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

        print(filtered_words)
        return words

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":

    print(sys.path)

    url_to_scrape = "https://www3.nhk.or.jp/news/easy/ne2025081511586/ne2025081511586.html"
    japanese_words = scrape_japanese_words(url_to_scrape)