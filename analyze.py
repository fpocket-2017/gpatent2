# coding: utf-8
import os
import codecs
import re

import xml.etree.ElementTree as et

import requests
import bs4

from  const import PATH_DIR_OUTPUT_TEXT
import utils

def readSearchWord(fp):
# If no search word exist, return "%all%"

    text = fp.read()
    sWords = []
    if re.search('\r', text):
        if re.search('\n', text):
            sWords = re.split("\r\n", text)
        else:
            sWords = re.split("\r", text)
    elif re.search('\n', text):
        sWords = re.split("\n", text)
    else:
        sWords.append(text)

    if sWords[len(sWords) - 1] == '':
        del sWords[len(sWords) - 1]

    return(sWords)

def html_analyze(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    section = soup.find(itemprop = u"description")
    if section != None:
        return(section.find(itemprop = u"content"))
    else:
        return(None)

def paragraphs_split(text):
    return(re.split(r"\n", text))

def word_search(root, sWords, paragraphs):
    for paragraph in paragraphs:
        for word in sWords:
            if re.search(word, paragraph) != None:
                p = et.SubElement(root, 'p')
                p.text = paragraph
                break

def analyze(root, sWords, pnum, url):
    fname = '{0}/{1}_{2}.txt'.format(PATH_DIR_OUTPUT_TEXT, pnum, 'd')
    if os.path.exists(fname):
        print('Text data is already exist')
        fp = codecs.open(fname, 'r', 'utf-8')
        paragraphs = paragraphs_split(fp.read())
        fp.close
    else:
        print('Getting Information from Patents.Google.com...')
        response = requests.get(url)
        print('Status Code: ' + str(response.status_code) + '\n')

        response.encoding = 'utf-8'
        
        description = html_analyze(response.text)

        if description == None:
            print('Description is not available\n')
            return()
        
        fp = codecs.open(fname, 'w', 'utf-8')
        fp.write(description.text)
        fp.close
        
        paragraphs = paragraphs_split(description.text)

    print('Analyzing...\n')
    word_search(root, sWords, paragraphs)
