# -*- coding: utf-8 -*-

'''
Created on 17 mar. 2022

@author: jose-lopez
'''
from pathlib import Path
import json
import math
import random
import sys

from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span, DocBin
from spacy.language import Language
import spacy


def load_jsonl(path):

    data = []

    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            if not line == "\n":
                data.append(json.loads(line))

    return data


def create_config_2(model_name: str, nlp: Language, components_to_update: list, output_path: Path):

    # create a new config as a copy of the loaded pipeline's config
    config = nlp.config.copy()

    # revert most training settings to the current defaults
    default_config = spacy.blank(nlp.lang).config
    config["corpora"] = default_config["corpora"]
    config["training"]["logger"] = default_config["training"]["logger"]

    # copy tokenizer and vocab settings from the base model, which includes
    # lookups (lexeme_norm) and vectors, so they don't need to be copied or
    # initialized separately
    config["initialize"]["before_init"] = {
        "@callbacks": "spacy.copy_from_base_model.v1",
        "tokenizer": model_name,
        "vocab": model_name,
    }
    config["initialize"]["lookups"] = None
    config["initialize"]["vectors"] = None

    # source all components from the loaded pipeline and freeze all except the
    # component to update; replace the listener for the component that is
    # being updated so that it can be updated independently
    config["training"]["frozen_components"] = []
    for pipe_name in nlp.component_names:
        if pipe_name not in components_to_update:
            config["components"][pipe_name] = {"source": model_name}
            config["training"]["frozen_components"].append(pipe_name)
        else:
            config["components"][pipe_name] = {
                "source": model_name,
                "replace_listeners": ["model.tok2vec"],
            }

    # save the config
    config.to_disk(output_path)


def create_config(model_name: str, nlp: Language, component_to_update: str, output_path: Path):

    # create a new config as a copy of the loaded pipeline's config
    config = nlp.config.copy()

    # revert most training settings to the current defaults
    default_config = spacy.blank(nlp.lang).config
    config["corpora"] = default_config["corpora"]
    config["training"]["logger"] = default_config["training"]["logger"]

    # copy tokenizer and vocab settings from the base model, which includes
    # lookups (lexeme_norm) and vectors, so they don't need to be copied or
    # initialized separately
    config["initialize"]["before_init"] = {
        "@callbacks": "spacy.copy_from_base_model.v1",
        "tokenizer": model_name,
        "vocab": model_name,
    }
    config["initialize"]["lookups"] = None
    config["initialize"]["vectors"] = None

    # source all components from the loaded pipeline and freeze all except the
    # component to update; replace the listener for the component that is
    # being updated so that it can be updated independently
    config["training"]["frozen_components"] = []
    for pipe_name in nlp.component_names:
        if pipe_name != component_to_update:
            config["components"][pipe_name] = {"source": model_name}
            config["training"]["frozen_components"].append(pipe_name)
        else:
            config["components"][pipe_name] = {
                "source": model_name,
                "replace_listeners": ["model.tok2vec"],
            }

    # save the config
    config.to_disk(output_path)

def setting_patterns(patterns, matcher):

    current_line = 1

    labels = ["PERSON", "PLACE", "GROUP", "WORK", "COUNTRY", "GOD"]

    for name_pattern in patterns:

        if name_pattern["label"] in labels:
            matcher.add(name_pattern["label"], [name_pattern["pattern"]])
            current_line += 1
        else:
            print("There is an error on label value at line: {}".format(
                current_line))
            sys.exit()


def setting_patterns_bio_objects(matcher, nlp):

    path_bio_objects = "data/bio_objects"

    categories = []

    bio_files = [str(x) for x in Path(path_bio_objects).glob("**/*")]

    line = 1

    for file in bio_files:

        line = 1

        with open(file, 'r', encoding="utf8") as f:
            bio_objects = [line.strip() for line in list(f.readlines())]

            for bio_object in bio_objects:
                synonyms = bio_object.split(";")
                CATEGORY = synonyms[0].upper()
                patterns = [doc for doc in nlp.pipe(synonyms)]
                if CATEGORY not in categories:
                    categories.append(CATEGORY)
                    matcher.add(CATEGORY, patterns)
                    line += 1
                else:
                    print(f'The category {CATEGORY} in the file {file} at line {line} is repeated, please check.')
                    sys.exit()

    return categories

def token_from_span_in(spans, current_span):

    already_present = False

    current_span_tokens = [t.i for t in current_span]

    for span in spans:

        span_tokens = [t.i for t in span]

        for token_index in span_tokens:
            if token_index in current_span_tokens:
                already_present = True

        if already_present is True:
            break

    return already_present


def tagging_file_sentences(sentences, matcher, nlp):

    no_entities_docs = []
    entities_docs = []
    
    propn_hash = nlp.vocab.strings["PROPN"]
    nnp_hash = nlp.vocab.strings["NNP"]

    for doc in nlp.pipe(sentences):

        matches = matcher(doc)
        doc.ents = []
        spans = []

        for match_id, start, end in matches:

            # A first attempt to add POS and TAG labels to those entities
            # whose names are a single word token (JAK3, CDR4, and so on)
            # We need to define multiword tokens to improve the POS and TAG labeling
            # so multiword entities' names and tokens be available here.

            if start == end - 1:
                doc[start].pos = propn_hash
                doc[start].tag = nnp_hash
                doc[start].pos_ = "PROPN"
                doc[start].tag_ = "NNP"

            # Below the code to tag the entities in the document on process..

            label_ = nlp.vocab.strings[match_id]

            current_span = Span(
                doc, start, end, label=label_)

            if not token_from_span_in(spans, current_span):
                spans.append(current_span)

        doc.ents = spans

        if doc.text:
            if doc.ents:
                entities_docs.append(doc)
            else:
                no_entities_docs.append(doc)

    return entities_docs, no_entities_docs

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
    
    # The arguments for this script must be typed (for instance) as follows:
    # --model=en_core_web_sm --corpus=data/corpus_sars_cov --components_to_update=ner,tagger --config_output_path=./config_ner.cfg
    # --model=en_core_web_sm --corpus=data/corpus_covid --components_to_update=ner,tagger --config_output_path=./config_ner.cfg

    if len(sys.argv) == 5:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        CORPUS_PATH = args[1].split("=")[1]
        COMPONENTS_TO_UPDATE = list(args[2].split("=")[1].split(","))
        CONFIG_OUTPUT_PATH = args[3].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    print("\n" + ">>>>>>> Starting the entities tagging..........." + "\n")

    print(f'Loading the model ({MODEL})....')
    nlp = spacy.load(MODEL)

    print("\t" + "The pipeline's components:")
    print(f'\t{nlp.pipe_names}')
    print(".. done" + "\n")

    print(f'Setting the patterns for the processing of ({CORPUS_PATH})....')
    # matcher = Matcher(nlp.vocab)
    matcher = PhraseMatcher(nlp.vocab)
    # patterns = load_jsonl(PATTERNS_PATH)
    # setting_patterns(patterns, matcher)
    categories = setting_patterns_bio_objects(matcher, nlp)
    print(categories)
    print(".. done" + "\n")

    print(f'Processing NER entities for the corpus at ({CORPUS_PATH})....')

    # Total of sentences in the corpus and the its list of files
    corpus_size, files = from_corpus(CORPUS_PATH)

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

            entities_docs, no_entities_docs = tagging_file_sentences(SENTENCES,
                                                                     matcher, nlp)
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

    create_config_2(MODEL, nlp, COMPONENTS_TO_UPDATE, Path(CONFIG_OUTPUT_PATH))

    print(".... done"+ "\n")

    print(f'For the fine tuning of your model, run the following command:')
    print(f'python -m spacy train ./config_ner.cfg --output ./model --paths.train ./train.spacy --paths.dev ./dev.spacy')

