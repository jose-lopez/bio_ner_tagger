'''
Created on 2 oct. 2022

@author: jose-lopez
'''
from spacy.symbols import nsubj, VERB, dobj
import spacy
from spacy.language import Language
from spacy.tokens import Token

from pathlib import Path
import sys


class Builder(object):
    '''
    The class with the methods for the building of the knowledge base.
    '''

    def __init__(self, model_name: str, corpus_path: str):
        '''
        Constructor
        '''
        # model to tune-up
        self.__model_name = model_name

        # The corpus of files to analyze when we are building the knowledge base.
        self.__corpus_path = corpus_path

        # Loading the fine-tuned model to process the sentences and build the knowledge base
        print(f'Loading the model ({model_name})....')
        self.__nlp = spacy.load(model_name)

    @property
    def model_name(self):
        return self.__model_name

    @model_name.setter
    def model_name(self, model_name: str):
        self.__model_name = model_name

    @property
    def nlp(self):
        return self.__nlp

    @nlp.setter
    def nlp(self, nlp: Language):
        self.__nlp = nlp

    def get_label(self, token: Token, entities: list):
        '''
        Returns an entity's label if a token is part of it.
        '''

        label_ = ""

        for entity in entities:

            entity_tokens = [t.i for t in entity]

            for token_index in entity_tokens:
                if token_index == token.i:
                    label_ = entity.label_
                    break

        return label_

    def get_regulatory_functions(self, relations_file_: str):
        '''
        This method returns the list of regulatory functions that we use to
        establish if a VERB on process, is part of the verbs listed in ./data/relations-functions.txt.
        '''

        relations = []

        with open(relations_file_, 'r', encoding="utf8") as rl:
                    LINES = [line.strip() for line in rl.readlines()]

        for line in LINES:
            if "------------" not in line:
                relations.append(line)

        return relations

    def getting_bio_objects_categories(self):
        '''
        This method returns the list of main names, for each one of the biological objects
        defined in ./data/bio_objects. Each line in a file in ./data/bio_objects describe
        one biological object and the first name in it, defines the main name and the category
        (or the NER label) for it.
        '''

        path_bio_objects = "data/bio_objects"

        categories = []

        bio_files = [str(x) for x in Path(path_bio_objects).glob("**/*")]

        for file in bio_files:

            line = 1

            with open(file, 'r', encoding="utf8") as f:
                bio_objects = [line.strip() for line in list(f.readlines())]

                for bio_object in bio_objects:
                    synonyms = bio_object.split(";")
                    CATEGORY = synonyms[0].upper()
                    if CATEGORY not in categories:
                        categories.append(CATEGORY)
                        line += 1
                    else:
                        print(f'The category {CATEGORY} in file {file} at line {line} is repeated')
                        sys.exit()

        return categories

    def get_events_sents_noun_phrases(self, files: list, nlp: Language, categories: list, relations: list):
        '''
        This is the main method used to discover regulatory events in a corpus.
        We have two options so far to accomplish this (the next method describes the second one).
        In this case we explore roots in the nominal phrases (noun chunk) of a sentence and, from there, we
        analyze if the root is a nsubj or a dobj. We check also if each root have a VERB as its head (parent node).
        If a nsubj and a dobj have the same VERB as its parent node, and the VERB is part of the biological relations
        that we are interested in, then a valid regulatory event has been detected.
        '''

        # The regulatory events and their related sentences
        events_sents = {}

        # The lists of subjects and objects to consider when trying to build up the regulatory events.
        # This must be carefully debugged from a linguistic point of view (must be improved)
        subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
        objects = ["dobj", "pobj", "dative", "attr", "oprd"]

        FILE_ON_PROCESS = 1

        if not len(files) == 0:

            for file_path in files:

                file_name = file_path.split("/")[2]

                print("\n" + f'..getting regulatory events from -> {file_name}: {FILE_ON_PROCESS} | {len(files)}' + "\n")

                with open(file_path, 'r', encoding="utf8") as fl:
                    SENTENCES = [line.strip() for line in fl.readlines()]

                    for doc in nlp.pipe(SENTENCES):
                        """
                        for entity in doc.ents:
                            if entity.start == entity.end - 1:
                                print(f'{doc[entity.start].text}  {doc[entity.start].pos_}  {doc[entity.start].tag_}  {doc[entity.start].dep_}')
                        """
                        # Finding a verb with a subject and a dobj related with it (all the possible ones)

                        for np_nsubj in doc.noun_chunks:
                            if np_nsubj.root.dep_ in subjects and np_nsubj.root.head.pos == VERB:
                                for np_dobj in doc.noun_chunks:
                                    if (np_dobj.root.dep_ in objects) and np_nsubj.root.head.pos == np_dobj.root.head.pos:
                                        # The lemmas and the token's head index must be the same for nsubj and the dobj, so they are really connected)
                                        if np_nsubj.root.head.lemma_ == np_dobj.root.head.lemma_ and np_nsubj.root.head.i == np_dobj.root.head.i:

                                            SUBJ = self.get_label(np_nsubj.root, doc.ents)
                                            OBJ = self.get_label(np_dobj.root, doc.ents)
                                            relation = np_nsubj.root.head.lemma_

                                            if SUBJ in categories and OBJ in categories and relation in relations:

                                                event = "event('{}',{},'{}')".format(SUBJ, relation, OBJ)
                                                # print(event)

                                                if event in events_sents.keys():
                                                    if doc.text not in events_sents[event]:
                                                        events_sents[event].append(doc.text)
                                                else:
                                                    events_sents[event] = [doc.text]
                                                    print(event)

                FILE_ON_PROCESS += 1

            print("\n" + "Corpus processing done" + "\n")

        return events_sents

    def get_events_sents(self, files: list, nlp: Language, categories: list, relations: list):
        '''
        This is the main method used to discover regulatory events in a corpus.
        We have two options so far to accomplish this (the method above describes the first one).
        In this case we define the possible nsubj(s) and dobj(s) in a sentence. We search
        for those nsubj(s) and a dobj(s) that have a VERB as its head (parent node).
        If a nsubj and a dobj have the same VERB as its parent node, and the VERB is part
        of the biological relations that we are interested in, then, a valid regulatory event has been detected.
        '''

        # The regulation events and their related sentences
        events_sents = {}

        # The lists of subjects and objects to consider when trying to build up the regulatory events
        # This must be carefully debugged from a linguistic point of view
        subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
        objects = ["dobj", "pobj", "dative", "attr", "oprd"]

        FILE_ON_PROCESS = 1

        if not len(files) == 0:

            for file_path in files:

                file_name = file_path.split("/")[2]

                print(
                    f'..getting regulatory events from -> {file_name}: {FILE_ON_PROCESS} | {len(files)}')

                with open(file_path, 'r', encoding="utf8") as fl:
                    SENTENCES = [line.strip() for line in fl.readlines()]

                    for doc in nlp.pipe(SENTENCES):

                        nsubjs = []
                        dobjs = []

                        for entity in doc.ents:
                            if entity.start == entity.end - 1:  # Only entities with only one token (by now).
                                # print(f'{doc[entity.start].text}  {doc[entity.start].pos_}  {doc[entity.start].tag_}  {doc[entity.start].dep_}  {doc[entity.start].head.text}  {doc[entity.start].head.pos_} {spacy.explain(doc[entity.start].head.pos_)}')
                                if doc[entity.start].dep_ in subjects:
                                    nsubjs.append(doc[entity.start].i)
                                elif doc[entity.start].dep_ in objects:
                                    dobjs.append(doc[entity.start].i)

                        # Finding a VERB token connecting the nsubjs and dobjs (all the possible ones)

                        for nsubj in nsubjs:
                            for dobj in dobjs:
                                if doc[nsubj].head == doc[dobj].head and doc[nsubj].head.pos == VERB:

                                    SUBJ = self.get_label(doc[nsubj], doc.ents)
                                    OBJ = self.get_label(doc[dobj], doc.ents)
                                    relation = self.in_relations(doc[nsubj].head.lemma_, relations)

                                    if SUBJ in categories and OBJ in categories and relation:

                                        event = "event('{}',{},'{}')".format(SUBJ, relation, OBJ)
                                        # print(event)

                                        if event in events_sents.keys():
                                            if doc.text not in events_sents[event]:
                                                events_sents[event].append(doc.text)
                                        else:
                                            events_sents[event] = [doc.text]
                                            print(event)

                FILE_ON_PROCESS += 1

        return events_sents
