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


def get_word_of_the_day():
    '''
    Get the word of the day from Britannica Dictionary

    Returns:
        dict: Dictionary containing the word, part of speech, image, and meaning information, or None if not found
    '''
    url = f"{DOMAIN}/dictionary/eb/word-of-the-day"
    soup = get_soup(url)
    
    if not soup:
        return None

    word_container = soup.find('div', class_='hw_d box_sizing ld_xs_hidden')
    image_container = soup.find('div', class_='wod_img_act')
    meaning_container = soup.find('div', class_='midbs')  # Container for meaning information

    word_info = {}

    if word_container:
        word_text = word_container.find('span', class_='hw_txt').get_text(strip=True)
        part_of_speech = word_container.find('span', class_='fl').get_text(strip=True)
        word_info['word'] = f"{word_text} ({part_of_speech})"
    else:
        return None

    if image_container:
        image = image_container.find('img')
        if image:
            word_info['image'] = {'src': image.get('src', ''), 'alt': image.get('alt', '')}

    if meaning_container:
        meanings = []
        meaning_blocks = meaning_container.find_all('div', class_='midb')
        for block in meaning_blocks:
            definition = block.find('div', class_='midbt').find('p').get_text(strip=False)
            examples = [example.get_text(strip=False) for example in block.find_all('li', class_='vi')]
            meaning = { 'definition': definition, 'examples': examples}
            meanings.append(meaning)
    word_info['meanings'] = meanings


    return word_info