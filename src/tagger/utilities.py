'''
Created on 1 oct. 2022

@author: jose-lopez
'''

from pathlib import Path
import sys

from spacy.language import Language
import spacy


class Utility:
    '''
    A class to make available some general methods
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def from_corpus(self, corpus_path: str):

        corpus_length = 0

        files_ = [str(x) for x in Path(corpus_path).glob("**/*.txt")]

        if files_:

            for file_path_ in files_:
                with open(file_path_, 'r', encoding="utf8") as f:
                    sentences = list(f.readlines())

                corpus_length += len(sentences)

        else:
            print(f'Not files at {corpus_path}')
            sys.exit()

        return corpus_length, files_
