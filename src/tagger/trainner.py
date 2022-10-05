'''
Created on 2 oct. 2022

@author: jose-lopez
'''
from pathlib import Path
import json

import sys
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span, DocBin
from spacy.language import Language
import spacy


class Trainner(object):
    '''
    This class relates is about the code to construct the set \
    of training and evaluation examples for the training (fine-tuning) of the NER component of a NLP \
    model for biological objects (entities) detection.
    '''

    def __init__(self, model_name: str, corpus_path: Path, components: list, config_path: Path):
        '''
        Constructor
        '''
        self.__model_name = model_name  # model to tune-up
        self.__corpus_path = corpus_path  # The corpus of files to tag to build the NER examples
        self.__components = components  # The components to tune up (tagger, ner, parser, and so on)
        self.__config_path = config_path  # The path to save the configuration file for training

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

    def load_jsonl(self, path: str):
        '''
        A method for the reading of .json files.
        '''
        data = []

        with open(path, 'r', encoding='utf-8') as reader:
            for line in reader:
                if not line == "\n":
                    data.append(json.loads(line))

        return data

    def create_config(self, model_name: str, nlp: Language, components_to_update: list, output_path: Path):
        '''
        This function allows the setting a the spacy's config.cfg file.
        There is a demo project that shows how to do this in this address:
        https://github.com/explosion/projects/tree/v3/pipelines/ner_demo_update
        The code below is a slightly different version that allows to train more than
        one component in a pipeline.
        '''
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

    def setting_patterns(self, patterns: str, matcher: Matcher):
        '''
        This code allows to load the patterns when we are using a matcher instead of phrase matcher.
        The text that we use to show how this code works is in ./data/corpus_en and the related
        file or patterns is in ./data/patterns.
        '''

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

    def setting_patterns_bio_objects(self, matcher: PhraseMatcher, nlp: Language):
        '''
        This code allows to load the patterns when we are using a phrasematcher instead of matcher.
        This is the option that we follow to process the corpus available in ./data/corpus_covid.
        '''

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

    def token_from_span_in(self, spans: list, current_span: Span):
        '''
        This a function to check if a token in a spacy span is already part of one of the entities (spans)
        of a sentence.
        '''

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

    def tagging_file_sentences(self, sentences: list, matcher: PhraseMatcher, nlp: Language):
        '''
        The method used to set the doc.ents in a set of spacy sentences (docs).
        In this method we also set those tokens in a sentence that correspond
        to the biological names available in ./data/bio_objects. Each line in a
        file in ./data/bio_objects defines the name of a biological object
        and its synonyms (separated by a colon). This method returns the subsets of sentences
        that have and don't entities (needed to fine-tune a model later).
        '''

        no_entities_docs = []  # Sentences that don't have entities.
        entities_docs = []  # Sentences that do have entities.

        propn_hash = nlp.vocab.strings["PROPN"]
        nnp_hash = nlp.vocab.strings["NNP"]

        for doc in nlp.pipe(sentences):

            matches = matcher(doc)
            doc.ents = []
            spans = []

            for match_id, start, end in matches:

                """
                A first attempt to add POS and TAG labels to single-token entities (JAK3, CDR4, etc.).
                Further on it is required to define multi-word tokens to improve the POS and TAG labeling
                for those names of biological objects composed of more than one word.
                """

                if start == end - 1:
                    doc[start].pos = propn_hash
                    doc[start].tag = nnp_hash
                    doc[start].pos_ = "PROPN"
                    doc[start].tag_ = "NNP"

                # Below the code to tag the entities in the document on process..

                label_ = nlp.vocab.strings[match_id]

                current_span = Span(
                    doc, start, end, label=label_)

                if not self.token_from_span_in(spans, current_span):
                    spans.append(current_span)

            doc.ents = spans

            if doc.text:
                if doc.ents:
                    entities_docs.append(doc)
                else:
                    no_entities_docs.append(doc)

        return entities_docs, no_entities_docs
