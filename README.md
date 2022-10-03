# bio_ner_tagger
An experiment to tag ner entities related with biological molecular species using spaCy, fine-tunning a spacy's pipeline, and building a knowledge base
of regulatory events, in order to model a gene regulatory network from them. Here we include the code to the ner tagging of examples, define 
the configuration file to fine-tune a spacy's model, and how to use the fine-tuned model to build up a knowledge base of regulatoru events.
The knowledge base is automatically organized based on the facilities that offers the fine-tuned model. The fine-tunning process include basic POS,
TAG and NER labelling. Our code, therefore, is about the fine-tuning of tagger and the ner pipeline's components.

There are two python scripts of interest here: setter.py and kb_constructor.py. The first one set the examples to fine-tune the model and defines the
configuration file to train (fine-tune) a spacy model (en_core_wb_sm, for instance)

In order tu run the python scripts hosted in this repository, please follow the next steps:

1. Install spaCy as you can see in:
https://spacy.io/usage#quickstart
Be sure of having Python 3.9 in your system. We recomend to use a virtual enviroment as the spacy's installation instructions shows.

2. 




