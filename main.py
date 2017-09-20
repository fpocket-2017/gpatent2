# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as et

import const

from file_system import readSearchWords, readPageUrls, writeResult
from utils       import url2pnum, indent
from analyze     import analyze

# Read search word(s)
search_words = readSearchWords(const.PATH_FILE_SEARCH_WORDS)

# Read page url(s)
urls = readPageUrls(const.PATH_FILE_PAGE_URLS)

# Load framework
tframework = et.ElementTree(file = const.PATH_FILE_FRAMEWORK)
root = tframework.getroot()

print('Collecting Text Information...\n')

for idx, url in enumerate(urls):
    # Load framework of child tree
    tchild = et.ElementTree(file= const.PATH_FILE_FRAMEWORK_CHILD)
    
    croot = tchild.getroot()

    # Set URL
    croot[0][0][0].set(u'href', url)
    croot[0][0][0].text = url
    
    if re.match(u'http', url) == None:
        print(u'{0}/{1} : {2}\n'.format(idx + 1, len(urls), url))
        print(u'URL is not correct\n')
        continue

    pnum = url2pnum(url)
    print(u'{0}/{1} : {2}\n'.format(idx + 1, len(urls), pnum))
    analyze(croot[0][1][1], search_words, pnum, url)

    root[1][0].append(croot)

indent(root)

# Write result
writeResult(const.PATH_DIR_OUTPUT, search_words, tframework)
