#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse
import sys
import json


__author__ = "Fangyao Liu"
__email__ = "fangyaoliu@g.ucla.edu"

# Some useful data.
_CONTRACTIONS = {
    "tis": "'tis",
    "aint": "ain't",
    "amnt": "amn't",
    "arent": "aren't",
    "cant": "can't",
    "couldve": "could've",
    "couldnt": "couldn't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "dont": "don't",
    "hadnt": "hadn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "hed": "he'd",
    "hell": "he'll",
    "hes": "he's",
    "howd": "how'd",
    "howll": "how'll",
    "hows": "how's",
    "id": "i'd",
    "ill": "i'll",
    "im": "i'm",
    "ive": "i've",
    "isnt": "isn't",
    "itd": "it'd",
    "itll": "it'll",
    "its": "it's",
    "mightnt": "mightn't",
    "mightve": "might've",
    "mustnt": "mustn't",
    "mustve": "must've",
    "neednt": "needn't",
    "oclock": "o'clock",
    "ol": "'ol",
    "oughtnt": "oughtn't",
    "shant": "shan't",
    "shed": "she'd",
    "shell": "she'll",
    "shes": "she's",
    "shouldve": "should've",
    "shouldnt": "shouldn't",
    "somebodys": "somebody's",
    "someones": "someone's",
    "somethings": "something's",
    "thatll": "that'll",
    "thats": "that's",
    "thatd": "that'd",
    "thered": "there'd",
    "therere": "there're",
    "theres": "there's",
    "theyd": "they'd",
    "theyll": "they'll",
    "theyre": "they're",
    "theyve": "they've",
    "wasnt": "wasn't",
    "wed": "we'd",
    "wedve": "wed've",
    "well": "we'll",
    "were": "we're",
    "weve": "we've",
    "werent": "weren't",
    "whatd": "what'd",
    "whatll": "what'll",
    "whatre": "what're",
    "whats": "what's",
    "whatve": "what've",
    "whens": "when's",
    "whered": "where'd",
    "wheres": "where's",
    "whereve": "where've",
    "whod": "who'd",
    "whodve": "whod've",
    "wholl": "who'll",
    "whore": "who're",
    "whos": "who's",
    "whove": "who've",
    "whyd": "why'd",
    "whyre": "why're",
    "whys": "why's",
    "wont": "won't",
    "wouldve": "would've",
    "wouldnt": "wouldn't",
    "yall": "y'all",
    "youd": "you'd",
    "youll": "you'll",
    "youre": "you're",
    "youve": "you've"
}

# You may need to write regular expressions.

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings 
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    # YOUR CODE GOES BELOW:
    # 1. Replace new lines and tab characters with a single space.
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # 2. Remove URLs
    text = re.sub('(http|https)?:\/(\/\S*)?', '', text)

    # 3. Split text on a single space. If there are multiple contiguous spaces,
    # you will need to remove empty tokens after doing the split.
    text = re.sub(' +', ' ', text)

    # 4. Separate all external punctuation such as periods, commas, etc.
    text=" "+text+" "
    text=list(text)
    for index in range(len(text)):
        if text[index] in string.punctuation:
            if(text[index+1] not in string.ascii_letters or text[index-1] not in string.ascii_letters) and (text[index+1] not in string.digits or text[index-1] not in string.digits):
                if not (text[index]=="$" and text[index+1] in string.digits ):
                    text[index]=" "+text[index]+" "
    del text[0]
    del text[-1]
    text = "".join(text)

    # 5. Remove all punctuations
    text = text.split(" ")
    while "" in text:
        text.remove("")
    remain_pun=[".", "!", "?", ":", ",", ";"]
    for index in range(len(text)):
        if text[index] in string.punctuation and text[index] not in remain_pun:
            text[index] = ""
    while "" in text:
        text.remove("")
    text = " ".join(text)

    # 6. Convert all text to lower cases
    text = text.lower()

    parsed_text = text

    text = re.sub(' \W+$', '', text)
    # 8. unigram
    unigram_text = re.sub(' \W ', ' ', text)
    unigram_text = re.sub(' \W ', ' ', unigram_text)

    # 8. bigram
    bigram_list = re.split(' \W ', text)
    bigrams = ""
    for sentence in bigram_list:
        sentence = sentence.lstrip()
        word_list = sentence.split(' ')
        length = len(word_list)
        if length < 2:
            continue
        for index in range(length - 1):
            bigrams = bigrams + " " + word_list[index] + "_" + word_list[index + 1]
    bigrams = bigrams.lstrip()
    bigram_text = bigrams

    # 8. trigram
    trigrams = ""
    for sentence in bigram_list:
        sentence = sentence.lstrip()
        word_list = sentence.split(' ')
        length = len(word_list)
        if length < 3:
            continue
        for index in range(length - 2):
            trigrams = trigrams + " " + word_list[index] + "_" + word_list[index + 1] + "_" + word_list[index + 2]
    trigrams = trigrams.lstrip()
    trigram_text = trigrams

    return [parsed_text, unigram_text, bigram_text, trigram_text]


if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.

    # YOUR CODE GOES BELOW.
    para = sys.argv
    json_file = para[1]
    with open(json_file, 'r') as f:
        try:
            for line in f:
                l = json.loads(line)
                target = l["body"]
                result = sanitize(target)
                print(result)
        except:
            f.close()

