# bio_ner_tagger
This is an NLP experiment about a) the POS, TAG, and NER tagging of sentences related with biological molecular species and their interactions, using the spaCy library, b) the fine-tuning of a spacy's pipeline with the tagged sentences, c) the identification of biological molecular species and their interactions in a corpus, and d) the construction of a knowledge base of regulatory events from them.

The fine-tuning process that we make includes basic POS, TAG and NER tagging. Our code is about the fine-tuning of the tagger and the NER pipeline's components. There are two python scripts of interest here: setter.py and kb_constructor.py. The first one sets the examples to fine-tune the model and defines the configuration file to train (fine-tune) a spacy model. The second script is related to the automatic building of a knowledge base of regulatory events from a set of regulatory sentences.

Below an example of the kind of knowledge base that we get:

base([

event('ACE2',bind,'SARS-COV'),

event('CD4',express,'CD4').

event('CD4',promote,'CCR5').

event('ACE2',bind,'SARS-COV-2'),

..

]).


Below are some sentences from where the regulatory events came from. Our work at the moment is about how to use linguistic features and the spacy's library linguistic facilities, in order to improve the detection of regulatory events in a sentence. It is possible to see below that there are some sentences with regulatory events (entitiies and their relationships), that our code isn't able to detect yet.

event('ACE2',bind,'SARS-COV').
Angiotensin-converting enzyme 2 (ACE2), the C-type lectin CD209L (also known L-SIGN), and DC-SIGN bind SARS-CoV, but ACE2 appears to be the key functional receptor for the virus.

event('CD4',express,'CD4').
CD4 and GHOST(3)-engineered to express stably CD4 and the chemokine receptors CCR1, CCR2b, CCR3, CCR5, or CXCR4, or the orphan receptors BOB/gpr15 or Bonzo/STRL33/TYMSTR.

event('CD4',promote,'CCR5').
Interaction of the human immunodeficiency virus type 1 (HIV-1) gp120 envelope glycoprotein with the primary receptor, CD4 promotes binding to a chemokine receptor, either CCR5 or CXCR4.

How to install and run our code:

In order to run the python scripts mentioned above, please follow the steps below:

1. Install spaCy as you can see in: https://spacy.io/usage#quickstart.
Be sure of having Python 3.9 in your system. We recommend using a virtual environment as the spacy's installation instructions describes.

2. Clone the project and set the PYTHONPATH variable in order to point to the source code of this project.

For instance:

$ git clone https://github.com/jose-lopez/bio_ner_tagger.git

$ export PYTHONPATH=$PYTHONPATH:$HOME/bio_ner_tagger/src

3. Change directory to the bio_ner_tagger folder.

4. To set the training and evaluation examples, and the fine-tuning configuration file, proceed as follows:

$ python src/tagger/setter.py --model=en_core_web_sm --corpus=data/corpus_sars_cov --components_to_update=ner,tagger --config_output_path=./config_ner.cfg

5. The steps above define the files train.spacy and dev.spacy, and the config_ner.cfg configuration file. In order to fine-tune a model, please run:

$ python -m spacy train ./config_ner.cfg --output ./model --paths.train ./train.spacy --paths.dev ./dev.spacy

6. The step above builds a new fine-tuned model in the ./model folder. You can use the fine-tuned model to build the knowledge base of regulatory events running line below:

$ python src/tagger/kb_constructor.py --model=model/model-best --corpus=data/corpus_sars_cov

7. The command line that we describe above will produce two files as output: kbase.pl and kbase.text, available in the data/knowledge_base folder. The kbase.pl file contains the set of regulatory events modeled and it is a Prolog style formatted file. The kbase.pl file defines a network of interactions and it is ready to be loaded in an inference system, in order to explore possible regulatory pathways. On the other hand, the kbase.txt file lists the regulatory events from kbase.pl, and offers the regulatory sentences from where the regulatory events are modeled. This repo offers two small sets of sentences to play with: the corpus_sars_cov and the corpus_covid; both of them available in the ./data projects's folder.
