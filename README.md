# bio_ner_tagger
An experiment to tag ner entities related with biological molecular species using spaCy, fine-tuning a spacy's pipeline, and building a knowledge base of regulatory events, in order to model a gene regulatory network from them. Here we include the code for the ner tagging of examples, define the configuration file to fine-tune a spacy's model, and how to use the fine-tuned model to build a knowledge base of regulatory events. The knowledge base is automatically organized based on the facilities available from the fine-tuned model.

The fine-tuning process includes basic POS, TAG and NER tagging. Our code is about the fine-tuning of the tagger and the ner pipeline's components.There are two python scripts of interest here: setter.py and kb_constructor.py. The first one set the examples to fine-tune the model and defines the configuration file to train (fine-tune) a spacy model (en_core_web_sm, for instance). The second script is related to the automatic building of a knowledge base of regulatory events.

In order to run the python scripts mentioned above, please follow the steps below:

1. Install spaCy as you can see in: https://spacy.io/usage#quickstart.
Be sure of having Python 3.9 in your system. We recomend to use a virtual environment as the spacy's installation instructions describes.

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

7. Two files are the output of the command line described above: kbase.pl and kbase.text, available in the data/knowledge_base folder. The kbase.pl file contains the set of regulatory events modeled and it is a Prolog style formatted file. The kbase.pl file is ready to be integrated in an inference system in order to explore possible regulatory pathways. On the other hand, the kbase.txt file list the regulatory events from kbase.pl, and offers the regulatory sentences from where the regulatory events are modeled. This repo offers two small sets of sentences to play with: the corpus_sars_cov and the corpus_covid; both of them avalilable in the ./data projects's folder.





