'''
Created on 8 ago. 2022

@author: jose-lopez
'''

from spacy.symbols import nsubj, VERB, dobj
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("HIV-1 preferentially infects CCR5 with high levels of CD4 and those subsets of T cells, HIV-1 express CCR5, particularly memory T cells.")

# Finding a verb with a subject and a dobj from below

for np_nsubj in doc.noun_chunks:
    if np_nsubj.root.dep == nsubj and np_nsubj.root.head.pos == VERB:
        for np_dobj in doc.noun_chunks:
            if np_dobj.root.dep == dobj and np_nsubj.root.head.pos == np_dobj.root.head.pos:
                
                if np_nsubj.root.head.lemma_ == np_dobj.root.head.lemma_:
                
                    print(
                        f'event("{np_nsubj.root.text}",{np_nsubj.root.head.lemma_},"{np_dobj.root.text})"')

for np in doc.noun_chunks:
    print(
        f'"{np.text}", {np.root.text}, {np.root.dep_}, "{spacy.explain(np.root.dep_)}", {np.root.head.text}, {np.root.head.pos_}')
