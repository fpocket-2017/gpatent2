# coding: utf-8
import os
import codecs
import re
import pdb

import xml.etree.ElementTree as et

import requests
import bs4

from  const import PATH_DIR_OUTPUT_TEXT
import utils

def htmlParse(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    section = soup.find(itemprop = u"description")
    if section != None:
        return(section.find(itemprop = u"content"))
    else:
        return(None)

def paragraphSplit(text):
    return(re.split(r"\n", text))

def wordSearch(root, search_words, paragraphs):
    for paragraph in paragraphs:
        for word in search_words:
            if re.search(word, paragraph) != None:
                p = et.SubElement(root, 'p')
                p.text = paragraph
                break

def analyze(root, search_words, pnum, url):
    fname = '{0}/{1}_{2}.txt'.format(PATH_DIR_OUTPUT_TEXT, pnum, 'd')

    if os.path.exists(fname):
        print(u'Text data is already exist')
        
        with codecs.open(fname, 'r', 'utf-8') as fp:
            text = fp.read()
    else:
        print('Getting Information from Patents.Google.com...')
        
        response = requests.get(url)
        print(u'Status Code: {0}\n'.format(str(response.status_code)))

        response.encoding = 'utf-8'
        
        description = htmlParse(response.text)

        if description == None:
            print('Description is not available\n')
            return()
        
        text = description.text
        with codecs.open(fname, 'w', 'utf-8') as fp:
            fp.write(text)

    paragraphs = paragraphSplit(text)

    print('Analyzing...\n')
    wordSearch(root, search_words, paragraphs)
