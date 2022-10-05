'''
Created on 2 oct. 2022

@author: jose-lopez

This script finds and reports the entities that are present in a corpus
in order to fine tune a spacy pipeline. In our work we are dealing with
biological objects described in ./data/bio-objects. Our goal in this code
is to set and save train and evaluation examples to fine-tune a spaCy pipeline.
This script also sets the config.cfg file required to fine-tune the pipeline later.

'''

from pathlib import Path
import math
import random
import sys

from spacy.matcher import PhraseMatcher
from spacy.tokens import Span, DocBin

from tagger.trainner import Trainner
from tagger.utilities import Utility


if __name__ == '__main__':

    # The arguments for this script must be typed (for instance) as follows:
    # --model=en_core_web_sm --corpus=data/corpus_sars_cov --components_to_update=ner,tagger --config_output_path=./config_ner.cfg
    # --model=en_core_web_sm --corpus=data/corpus_covid --components_to_update=ner,tagger --config_output_path=./config_ner.cfg

    if len(sys.argv) == 5:
        args = sys.argv[1:]
        MODEL_NAME = args[0].split("=")[1]
        CORPUS_PATH = args[1].split("=")[1]
        COMPONENTS_TO_UPDATE = list(args[2].split("=")[1].split(","))
        CONFIG_OUTPUT_PATH = args[3].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    utilities = Utility()  # This object makes available some general propose methods

    # A trainer class object with the methods to set the NER examples and the configuration file.
    trainner = Trainner(MODEL_NAME, CORPUS_PATH, COMPONENTS_TO_UPDATE, Path(CONFIG_OUTPUT_PATH))

    print("\n" + ">>>>>>> Starting the entities tagging..........." + "\n")

    print("\t" + "The pipeline's components:")
    print(f'\t{trainner.nlp.pipe_names}')
    print(".. done" + "\n")

    print(f'Setting the patterns for the processing of ({CORPUS_PATH})....')

    # matcher = Matcher(nlp.vocab) # For the matcher option, not the phrasematcher
    # patterns = load_jsonl(PATTERNS_PATH) # For the matcher option, not the phrasematcher
    # setting_patterns(patterns, matcher) # For the matcher option

    phrase_matcher = PhraseMatcher(trainner.nlp.vocab)  # Building the phrasematcher

    # Getting the biological objects' categories and setting the phrasematcher's patterns
    categories = trainner.setting_patterns_bio_objects(phrase_matcher, trainner.nlp)
    # print(categories)
    print(".. done" + "\n")

    print(f'Processing NER entities for the corpus at ({CORPUS_PATH})....')

    # Total of sentences in the corpus and its list of files
    corpus_size, files = utilities.from_corpus(CORPUS_PATH)

    with_entities = []
    with_out_entities = []

    FILE_ON_PROCESS = 1

    if not len(files) == 0:

        for file_path in files:

            file_name = file_path.split("/")[2]

            with open(file_path, 'r', encoding="utf8") as fl:
                SENTENCES = [line.strip() for line in fl.readlines()]

            print(
                f'..tagging entities for -> {file_name}: {FILE_ON_PROCESS} | {len(files)}')

            entities_docs, no_entities_docs = trainner.tagging_file_sentences(SENTENCES, phrase_matcher, trainner.nlp)
            with_entities += entities_docs
            with_out_entities += no_entities_docs

            FILE_ON_PROCESS += 1

        print(".... done")

        print(
            f'Sentences: {corpus_size}; with entities|without_entities: {len(with_entities)}|{len(with_out_entities)}')

        docs = with_entities + with_out_entities

        random.shuffle(docs)

        training_samples = math.floor(len(docs) * 0.95)

        train_docs = docs[:training_samples]
        dev_docs = docs[training_samples:]

        print(
            f'Saving the training and evaluation sentences at ./train.spacy and ./dev.spacy')

        train_docbin = DocBin(docs=train_docs)
        train_docbin.to_disk("./train.spacy")

        dev_docbin = DocBin(docs=dev_docs)
        dev_docbin.to_disk("./dev.spacy")

    else:

        print("No files to tag. Please check the contents in the data/corpus folder" + "\n")
        sys.exit()

    print("\n" + ">>>>>>> Entities tagging finished..........." + "\n" + "\n")

    print(f'Creating the configuration file for training at ./config_ner.cfg')

    trainner.create_config(MODEL_NAME, trainner.nlp, COMPONENTS_TO_UPDATE, Path(CONFIG_OUTPUT_PATH))

    print(".... done" + "\n")

    print(f'For the fine tuning of your model, run the following command:')
    print(f'python -m spacy train ./config_ner.cfg --output ./model --paths.train ./train.spacy --paths.dev ./dev.spacy')
