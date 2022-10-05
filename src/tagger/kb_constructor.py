'''

Created on 2 oct. 2022

@author: jose-lopez

This script includes the necessary steps to build and report a knowledge base
constructed from a corpus of regulatory sentences, available in ./data.
An object of the Builder class offers the required methods to fulfill
the construction of the knowledge base.

'''

import sys

from tagger.builder import Builder
from tagger.utilities import Utility


if __name__ == '__main__':

    # The arguments to pass on to build the knowledge base using the trained model
    # --model=model/model-best --corpus=data/corpus_covid
    # --model=model/model-best --corpus=data/corpus_sars_cov

    # Paths to the knowledge base (in prolog format and documented)
    path_to_kb = "data/knowledge_base/kBase.pl"
    path_to_kb_doc = "data/knowledge_base/kBase.txt"

    # Path to the relations-functions file
    relations_file = "data/relations/relations-functions.txt"

    # This object makes available some general propose methods
    utilities = Utility()

    # getting the arguments
    if len(sys.argv) == 3:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        CORPUS_PATH = args[1].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    print("\n" + ">>>>>>> Starting the knowledge base modeling..........." + "\n")

    # A Builder class object with the methods to construct the knowledge base.
    builder = Builder(MODEL, CORPUS_PATH)

    print("\t" + "The pipeline's components are:")
    print(f'\t{builder.nlp.pipe_names}')
    print(".. done" + "\n")

    # Getting the corpus' amount of sentences and the path to each related file
    corpus_size, files = utilities.from_corpus(CORPUS_PATH)

    # Getting the relations to check when an event is on validation
    relations = builder.get_regulatory_functions(relations_file)

    # Getting the categories of biological objects
    categories = builder.getting_bio_objects_categories()

    print(f'Processing regulatory events from the corpus at ({CORPUS_PATH})....')

    # Using the noun phrases option
    events_sents = builder.get_events_sents_noun_phrases(files, builder.nlp, categories, relations)

    # Using the token.head option
    # events_sents = builder.get_events_sents(files, builder.nlp, categories, relations)

    if events_sents.keys():

        print(f'Printing the knowledge base of regulatory events at: {path_to_kb}' + "\n")

        with open(path_to_kb, 'w', encoding="utf8") as fd:

            fd.write("base([" + "\n")

            events = list(events_sents.keys())

            for event_ in events[:-1]:
                fd.write(event_ + "," + "\n")
            else:
                fd.write(events[-1] + "\n" + "]).")

        print(".. done" + "\n")

        print(f'Printing the documented knowledge base of regulatory events at: {path_to_kb_doc}' + "\n")

        with open(path_to_kb_doc, 'w', encoding="utf8") as fd:

            for event, sentences in events_sents.items():

                fd.write(event + "." + "\n")

                for sentence in sentences[:-1]:
                    fd.write(sentence + "\n")
                else:
                    fd.write(sentences[-1] + "\n")

        print(".. done" + "\n")

        print(f'Total of regulatory events = {len(events_sents.keys())}' + "\n")

        print(f'Knowledge base modeling finished !!!....')
    else:
        print(f'There are not regulatory events in the corpus at: {CORPUS_PATH}')
