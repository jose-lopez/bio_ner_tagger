'''
Created on 8 ago. 2022

@author: jose-lopez
'''

from spacy.symbols import nsubj, VERB, dobj
import spacy
from tagger.builder import Builder

MODEL = "model/model-best"
CORPUS_PATH = "data/corpus_sars_cov"

# Possible subjects and objects to check when we are exploring a possible regulatory event
subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
objects = ["dobj", "pobj", "dative", "attr", "oprd"]

# Path to the relations-functions file
relations_file = "data/relations/relations-functions.txt"

builder = Builder(MODEL, CORPUS_PATH)

# Getting the relations to check when an event is on validation
relations = builder.get_regulatory_functions(relations_file)

# Getting the categories of biological objects
categories = builder.getting_bio_objects_categories()

doc = builder.nlp("HIV-1 preferentially infects CCR5 with high levels of CD4 and those subsets of T cells, HIV-1 express CCR5, particularly memory T cells.")

# Finding a verb with a subject and a dobj connected to it.

for np_nsubj in doc.noun_chunks:
    if (np_nsubj.root.dep_ in subjects) and np_nsubj.root.head.pos == VERB:
        for np_dobj in doc.noun_chunks:
            if (np_dobj.root.dep_ in objects) and np_nsubj.root.head.pos == np_dobj.root.head.pos:
                # The lemma and the head's token index must be the same for nsubj and the dobj, so they are really connected)
                if np_nsubj.root.head.lemma_ == np_dobj.root.head.lemma_ and np_nsubj.root.head.i == np_dobj.root.head.i:

                    SUBJ = builder.get_label(np_nsubj.root, doc.ents)
                    OBJ = builder.get_label(np_dobj.root, doc.ents)
                    relation = np_nsubj.root.head.lemma_

                    if SUBJ in categories and OBJ in categories and relation in relations:

                        event = "event('{}',{},'{}')".format(SUBJ, relation, OBJ)
                        print(event)

for np in doc.noun_chunks:
    print(
        f'"{np.text}", {np.root.text}, {np.root.dep_}, "{spacy.explain(np.root.dep_)}", {np.root.head.text}, {np.root.head.pos_}')
