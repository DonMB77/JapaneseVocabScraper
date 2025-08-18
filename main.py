import requests
from bs4 import BeautifulSoup
import nagisa
import sys

from numpy.ma.core import count


def scrape_japanese_words(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all text content on the page
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


# Example usage:
if __name__ == "__main__":

    print(sys.path)

    # Replace with the URL you want to scrape
    url_to_scrape = "https://www3.nhk.or.jp/news/easy/ne2025081511586/ne2025081511586.html"

    # Run the scraper
    japanese_words = scrape_japanese_words(url_to_scrape)

    # Print the results
    if japanese_words:
        print(japanese_words)
        #for word in japanese_words:
        #    print(word)
    else:
        print("No Japanese words found or an error occurred.")