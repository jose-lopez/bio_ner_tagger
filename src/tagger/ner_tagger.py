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

from spacy.matcher import Matcher
from spacy.tokens import Span, DocBin
import spacy


def load_jsonl(path):

    data = []

    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            if not line == "\n":
                data.append(json.loads(line))

    return data


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

    for doc in nlp.pipe(sentences):

        matches = matcher(doc)
        doc.ents = []
        spans = []

        for match_id, start, end in matches:

            label_ = nlp.vocab.strings[match_id]

            current_span = Span(
                doc, start, end, label=label_)

            if not token_from_span_in(spans, current_span):
                spans.append(current_span)

        doc.ents = spans

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

    if len(sys.argv) == 4:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        PATTERNS_PATH = args[1].split("=")[1]
        CORPUS_PATH = args[2].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    print("\n" + ">>>>>>> Starting the entities tagging..........." + "\n")

    print(f'Loading the model ({MODEL})....')
    nlp = spacy.load(MODEL)
    print(".. done" + "\n")

    print(f'Loading the patterns ({PATTERNS_PATH})....')
    matcher = Matcher(nlp.vocab)
    patterns = load_jsonl(PATTERNS_PATH)
    setting_patterns(patterns, matcher)
    print(".. done" + "\n")

    print(f'Processing the corpus ({CORPUS_PATH})....')

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

        training_samples = math.floor(len(docs) * 0.7)

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

    print("\n" + ">>>>>>> Entities tagging finished...........")
