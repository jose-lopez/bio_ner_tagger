'''
Created on 15 ago. 2022

@author: jose-lopez
'''

from spacy.symbols import nsubj, VERB, dobj
import spacy

from pathlib import Path
import json
import math
import random
import sys


def from_corpus(CORPUS_PATH):

    corpus_length = 0

    files_ = [str(x) for x in Path(CORPUS_PATH).glob("**/*.txt")]

    if files_:

        for file_path_ in files_:
            with open(file_path_, 'r', encoding="utf8") as f:
                sentences = list(f.readlines())

            corpus_length += len(sentences)

    else:
        print(f'Not files at {CORPUS_PATH}')
        sys.exit()

    return corpus_length, files_

if __name__ == '__main__':

    if len(sys.argv) == 3:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        CORPUS_PATH = args[1].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    nlp = spacy.load(MODEL)

    corpus_size, files = from_corpus(CORPUS_PATH)
    # Finding a verb with a subject and a dobj from below
    # A sentence can have more than one subject and dobj

    FILE_ON_PROCESS = 1

    if not len(files) == 0:

        for file_path in files:

            file_name = file_path.split("/")[2]

            print(f'processing {file_name}')

            with open(file_path, 'r', encoding="utf8") as fl:
                SENTENCES = [line.strip() for line in fl.readlines()]

                for doc in nlp.pipe(SENTENCES):

                    for np_nsubj in doc.noun_chunks:
                        if np_nsubj.root.dep == nsubj and np_nsubj.root.head.pos == VERB:
                            for np_dobj in doc.noun_chunks:
                                if np_dobj.root.dep == dobj and np_nsubj.root.head.pos == np_dobj.root.head.pos:

                                    if np_nsubj.root.head.lemma_ == np_dobj.root.head.lemma_:

                                        print(doc.text)   
                                        print(
                                            f'event("{np_nsubj.root.text}",{np_nsubj.root.head.lemma_},"{np_dobj.root.text}")')
                                        print(
                                            f'"nominal subject": {np_nsubj.text}, "direct object": {np_dobj.text}')
                                        