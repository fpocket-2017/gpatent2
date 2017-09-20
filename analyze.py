# coding: utf-8
import os
import codecs
import re
import pdb

import xml.etree.ElementTree as et

import requests
import bs4

import const
import utils

def extractDescription(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    section = soup.find(itemprop = u'description')
    if section != None:
        return(section.find(itemprop = u'content'))
    else:
        return(None)

def paragraphSplit(text):
    return(re.split(r'\n', text))

def wordSearch(root, words, paragraphs):
    for paragraph in paragraphs:
        for word in words:
            if re.search(word, paragraph) != None:
                p = et.SubElement(root, 'p')
                p.text = paragraph
                break

def analyze(root, search_words, pnum, url):
    fname = '{0}/{1}.html'.format(const.PATH_DIR_OUTPUT_HTML, pnum)

    if os.path.exists(fname):
        print(u'HTML data is already exist')
        
        with codecs.open(fname, 'r', 'utf-8') as fp:
            html = fp.read()
    else:
        print('Getting Information from Patents.Google.com...')
        
        response = requests.get(url)
        print(u'Status Code: {0}\n'.format(str(response.status_code)))

        response.encoding = 'utf-8'

        html = response.text

        with codecs.open(fname, 'w', 'utf-8') as fp:
            fp.write(html)
    
    description = extractDescription(html)

    if description != None:
        fname = '{0}/{1}.txt'.format(const.PATH_DIR_OUTPUT_TEXT_DESCRIPTION, pnum)
        with codecs.open(fname, 'w', 'utf-8') as fp:
                fp.write(html)

        print('Analyzing...\n')
        paragraphs = paragraphSplit(description.text)
        wordSearch(root, search_words, paragraphs)
    else:
        print('Description is not available\n')
