# britannica.py
'''
Module for Britannica Dictionary

'''

import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://www.britannica.com'

def get_soup(url):
    '''
    Get BeautifulSoup object for a URL

    Args:
        url (str): URL to fetch and parse

    Returns:
        BeautifulSoup: BeautifulSoup object for the URL, or None if unable to retrieve
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_entries(word):
    '''
    Get related entries for a word in Britannica Dictionary

    Args:
        word (str): Word to search for

    Returns:
        list: List of dictionaries containing the text and link of each entry, or an empty list if no entries are found
    '''
    url = f"{DOMAIN}/dictionary/{word}"
    soup = get_soup(url)
    if not soup:
        return []
    entries = soup.find('ul', class_='o_list')

    if entries:
        return [{'text': entry.find('a').get_text(strip=True), 'link': DOMAIN + entry.find('a')['href']} for entry in entries.find_all('li')]
    else:
        return []

def get_total_entries(word):
    '''
    Get total number of entries for a word in Britannica Dictionary

    Args:
        word (str): Word to search for

    Returns:
        int: Total number of entries for the word
    '''
    return len(get_entries(word))


print(get_entries('apple'))