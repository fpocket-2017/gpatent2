# -*- coding: utf-8 -*-

import pandas as pd

def readSearchWords(
    path
    ):

    df = pd.read_csv(
            path,
            encoding = 'utf-8',
            header   = None
            )

    return df.iloc[:, 0].tolist()

def readPageUrls(
    path
    ):

    df = pd.read_csv(
            path,
            encoding = 'utf-8',
            skiprows = 1
            )

    return df.loc[:, "result link"].tolist()
    
def writeResult(
    path_dir_output,
    search_words,
    element_tree
    ):
    

    # Create output file name
    if search_words[0] == '':
        fname_output = 'all.html'
    else:
        fname_output = search_words[0]
        if len(search_words) > 1:
            for idx in range(1, len(search_words)):
                fname_output += u'_{0}'.format(search_words[idx])

        fname_output += '.html'

    element_tree.write(
        u'{0}/{1}'.format(path_dir_output, fname_output),
        encoding        = 'utf-8',
        xml_declaration = False
        )