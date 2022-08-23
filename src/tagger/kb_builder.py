'''
Created on 15 ago. 2022

@author: jose-lopez
'''

from spacy.symbols import nsubj, VERB, dobj
import spacy

from pathlib import Path
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


def get_label(token, entities):

    label_ = ""

    for entity in entities:

        entity_tokens = [t.i for t in entity]

        for token_index in entity_tokens:
            if token_index == token.i:
                label_ = entity.label_
                break

    return label_


def get_regulatory_functions(relations_file_):

    relations = []

    with open(relations_file_, 'r', encoding="utf8") as rl:
                LINES = [line.strip() for line in rl.readlines()]

    for line in LINES:
        if "------------" not in line:
            relations.append(line)

    return relations


def in_relations(relation_, relations_):

    in_relation = ""

    for r in relations_:
        if relation_ in r:
            in_relation = relation_
            break

    return in_relation


def getting_bio_objects_categories():

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
                    print(f'The category {CATEGORY} in the file {file} at line {line} is repeated')
                    sys.exit()

    return categories


if __name__ == '__main__':

    # Paths to the knowledge base (in prolog format and documented)
    path_to_kb = "data/knowledge_base/kBase.pl"
    path_to_kb_doc = "data/knowledge_base/kBase.txt"
    # Path to the relations-functions file
    relations_file = "data/relations/relations-functions.txt"

    # The regulation events and their related sentences
    events_sents = {}

    # getting the arguments
    if len(sys.argv) == 3:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        CORPUS_PATH = args[1].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    print("\n" + ">>>>>>> Starting the knowledge base modeling..........." + "\n")

    # Loading the model
    print(f'Loading the model ({MODEL})....')
    nlp = spacy.load(MODEL)

    print("\t" + "The pipeline's components are:")
    print(f'\t{nlp.pipe_names}')
    print(".. done" + "\n")

    # Getting the corpus amount of sentences and the path to each related file
    corpus_size, files = from_corpus(CORPUS_PATH)

    # Getting the relations to check when an event is on validation
    relations = get_regulatory_functions(relations_file)

    # Getting the categories of biological objects
    categories = getting_bio_objects_categories()

    print(f'Processing regulation events from the corpus at ({CORPUS_PATH})....')

    FILE_ON_PROCESS = 1

    if not len(files) == 0:

        for file_path in files:

            file_name = file_path.split("/")[2]

            print(
                f'..getting regulation events from -> {file_name}: {FILE_ON_PROCESS} | {len(files)}')

            with open(file_path, 'r', encoding="utf8") as fl:
                SENTENCES = [line.strip() for line in fl.readlines()]

                for doc in nlp.pipe(SENTENCES):

                    # Finding a verb with a subject and a dobj from below (all the possible ones)

                    for np_nsubj in doc.noun_chunks:
                        if np_nsubj.root.dep == nsubj and np_nsubj.root.head.pos == VERB:
                            for np_dobj in doc.noun_chunks:
                                if np_dobj.root.dep == dobj and np_nsubj.root.head.pos == np_dobj.root.head.pos:
                                    # The lemma and the head's token index must be the same for nsubj and the dobj, so they are really connected)
                                    if np_nsubj.root.head.lemma_ == np_dobj.root.head.lemma_ and np_nsubj.root.head.i == np_dobj.root.head.i:

                                        SUBJ = get_label(np_nsubj.root, doc.ents)
                                        OBJ = get_label(np_dobj.root, doc.ents)
                                        relation = in_relations(np_nsubj.root.head.lemma_, relations)

                                        # print(doc.text)

                                        if SUBJ in categories and OBJ in categories and relation:

                                            # event = "event(" + SUBJ + "," + relation + "," + OBJ + ")"

                                            event = "event('{}',{},'{}')".format(SUBJ, relation, OBJ)

                                            if event in events_sents.keys():
                                                if doc.text not in events_sents[event]:
                                                    events_sents[event].add(doc.text)
                                            else:
                                                events_sents[event] = [doc.text]
                                                print(event)
                                                

            FILE_ON_PROCESS += 1

        print(f'Printing the knowledge base of regulation events at: {path_to_kb}' + "\n")

        if events_sents.keys():

            with open(path_to_kb, 'w', encoding="utf8") as fd:

                fd.write("base([" + "\n")

                events = list(events_sents.keys())

                for event_ in events[:-1]:
                    fd.write(event_ + "," + "\n")
                else:
                    fd.write(events[-1] + "\n" + "]).")

            print(f'Printing the documented knowledge base of regulation events at: {path_to_kb_doc}' + "\n")

            with open(path_to_kb_doc, 'w', encoding="utf8") as fd:

                for event, sentences in events_sents.items():

                    fd.write(event + "." + "\n")

                    for sentence in sentences[:-1]:
                        fd.write(sentence + "\n")
                    else:
                        fd.write(sentences[-1] + "\n")

        print(f'Knowledge base processing done !!!....')
