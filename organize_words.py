# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 14:12:19 2021

@author: anany
"""

import string

FILEPATH = "C:/Users/anany/OneDrive/Desktop/webscraping/"
filename = "words.txt"

hashed_dictionary = {}

with open(FILEPATH + filename) as dictionary:
    for line in dictionary:
        line = line.lower().strip()
        
        if (len(line) <= 3):
            continue
        
        if any([char.isdigit() for char in line]):
            continue
        
        if any(char in string.punctuation for char in line):
            continue
        
        else:
            key = line[0]
            if key in hashed_dictionary.keys():
                hashed_dictionary[key].append(line)
            else:
                hashed_dictionary[key] = []
                hashed_dictionary[key].append(line)