# Project Name: Japanese Vocab Scraper

### Video Demo:  <URL HERE>
## Basic Description of Features:
This is a fairly simple web application aimed at improving your ability to learn new vocabulary from any given website.
One of the more frustrating tasks of learning a language is going through a webpage and manually extracting any vocabulary you want to learn. This app aims to fix that.

In order to explain the features, I will go through the two pages that make up this application.

#### Home:
Upon first entering this site, you can input any URL to scrape Japanese vocabulary from. After entering a URL, all non-Japanese words are discarded.
Then, all fetched words are displayed in a table. Only 5 words are printed per page, since words are translated at the time of printing to limit the stress put on the API used for translating.
Fetched words are printed along with their translation, their furigana (non-kanji reading), and word type (adjective, verb, etc.). In addition, you will see two buttons. One is used to display all the details of the word in a format
that enables you to easily copy all information into a learning app. It prints the word, furigana, and word type on one row, and the translation on another, just like you would format it on a flip card.
The other button saves that word in an internal database, which prevents the exact word from being fetched when another URL is inserted. This is to make sure you concentrate on only new vocabulary.
The red button on this page is used to redirect to the initial form to input another URL.

#### Vocab (Database):
On this page, you can see all saved vocabulary as previously explained in the homepage section. You can see the same information for every vocabulary word.
In addition, you can query the internal database for any saved word using the search bar at the top.
If you need to delete any word so it can be fetched again when entering a URL, you can use the delete button. Sometimes you might want to insert a word without specifically fetching it from a site.
For that, there is a form at the bottom of the table. If for some reason you want to start over with your saved vocab, there is a clear database button. But be careful! When this is clicked, there is no way of restoring the data!

## Technical Details:
This app is built using Flask (https://flask.palletsprojects.com) as its backend. The frontend is built using a relatively simple HTML, JavaScript, and CSS combination, while using Flask’s templates. Thus, it is written in Python.
In order to use this app on any screen size, Bootstrap has been used. Next, a quick explanation of the files and some implementation decisions:

#### main.py:
This is the main Flask application file for the Japanese Vocab Scraper project. It provides a web interface for scraping, displaying, translating, and managing Japanese vocabulary words.
The translation and word processing are not done here. This file is primarily used for routing and working with its two internal databases. There is one database for all saved vocabularies and one for all fetched words, which is cleared each time a new URL is scraped.

#### util/data_proccessing_unit.py:
This is a utility module for the project. It provides functions for processing, filtering, and translating Japanese vocabulary extracted from web pages. It uses `requests` to get the requested URL. BeautifulSoup is utilized to parse the given request into a tree structure that can be queried.
Afterwards, nagisa is employed to split the given text into its distinctive words. The exact dependencies and libraries are explained in more detail further below.

#### templates/:
In here all the different HTML files and templates are stored.

#### static/:
Here, all CSS is saved that is then used to style the pages in `templates/`.

## Dependencies:

#### requests (https://pypi.org/project/requests/):
The `requests` library is a popular Python package used for making HTTP requests to web servers. It allows you to send HTTP requests (such as GET, POST, PUT, DELETE) and handle responses in a user-friendly way.

#### beautifulsoup4 (https://pypi.org/project/beautifulsoup4/):
The `beautifulsoup4` library is a popular Python package for parsing and navigating HTML and XML documents. It allows you to extract data from web pages by converting the HTML into a tree structure that you can search and modify.

#### nagisa (https://github.com/taishi-i/nagisa):
The `nagisa` library is a Python package for Japanese natural language processing (NLP), specifically designed for tokenizing (splitting) Japanese text into words and assigning part-of-speech tags to each word. 
This excellent package was created by taishi-i. Without his incredible work, this project would have been impossible to make!

#### jisho (https://jisho.org/):
The Jisho API used in this project is an unofficial REST API for jisho.org, a popular online Japanese-English dictionary. It allows you to programmatically search for Japanese words and retrieve their English meanings and readings (furigana).
Jisho is truly amazing and is the website that has aided me the most when learning Japanese!
