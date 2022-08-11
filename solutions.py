# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 11:48:53 2021

@author: anany
"""
#!/usr/bin/python
import time
from selenium import webdriver
import re
import string

import sys
sys.path.append('C:/Users/anany/OneDrive/Desktop/webscraping')
import organize_words

# define functions to determine matches
def center_match(word, center, outers):
    for letter in word:
        if letter != center and letter not in outers:
            return False
    
    return True

def outer_match(word, center, outers):
    if center not in word:
        return False
    
    for letter in word:
        if letter != center and letter not in outers:
            return False
    
    return True

def isPangram(word, letters):
    for letter in letters:
        if letter not in word:
            return False
    
    return True

# open the website
DRIVER_PATH = "C:/Users/anany/OneDrive/Desktop/webscraping/chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.nytimes.com/puzzles/spelling-bee')
time.sleep(3)

button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/section[2]/div/div/div/div[2]/button[1]')
button.click()
time.sleep(3)

# scrape the center letter and outer letters
center_letter_element = driver.find_element_by_css_selector('#pz-game-root > div > div.sb-controls-box > div > div.sb-hive > div > svg.hive-cell.center > text')
center_letter = center_letter_element.text.lower()

outer_letter_elements = driver.find_elements_by_css_selector('#pz-game-root > div > div.sb-controls-box > div > div.sb-hive > div > svg.hive-cell.outer > text')
outer_letters = []
for element in outer_letter_elements:
    if (element.text != center_letter):
        outer_letters.append(element.text.lower())

# concatenate all letters into a single list
all_letters = outer_letters.copy()
all_letters.append(center_letter)

# scrape answers from website
element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/script')
text = element.get_attribute('innerHTML')

# record highest possible score
score = 0
record_words = False
answers = set()
pangrams = []
for word in re.split(':|,', text):
    word = word.translate(str.maketrans('', '', string.punctuation))
    
    if word == "id":
        break
    
    if (record_words):
        answers.add(word)
        
        if len(word) == 4:
            score += 1
        
        elif (isPangram(word, all_letters)):
            pangrams.append(word)
            score += 15
        
        else:
            score += len(word)
        
    if word == "answers":
        record_words = True

# retrieve all possible words from a dictionary
possible_words = set()
for letter in all_letters:
    if letter == center_letter:
        for word in organize_words.hashed_dictionary[center_letter]:
            if center_match(word, center_letter, outer_letters):
                possible_words.add(word)
    else:
        for word in organize_words.hashed_dictionary[letter]:
            if outer_match(word, center_letter, outer_letters):
                possible_words.add(word)

#possible_words = set(sorted(possible_words))
print("The answers are:", sorted(answers))
print("The pangrams are:", sorted(pangrams))
print("The other possibilities are:", sorted(possible_words.difference(answers)))
print("The highest score:", score)