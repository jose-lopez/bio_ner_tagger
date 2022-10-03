# bio_ner_tagger
An experiment to tag ner entities related with biological molecular species using spaCy, fine-tuning a spacy's pipeline, and building a knowledge base of regulatory events, in order to model a gene regulatory network from them. Here we include the code to the ner tagging of examples, define the configuration file to fine-tune a spacy's model, and how to use the fine-tuned model to build up a knowledge base of regulatory events. The knowledge base is automatically organized based on the facilities that offer the fine-tuned model.

The fine-tuning process includes basic POS, TAG and NER labelling. Our code is about the fine-tuning of tagger and the ner pipeline's components.There are two python scripts of interest here: setter.py and kb_constructor.py. The first one set the examples to fine-tune the model and defines the configuration file to train (fine-tune) a spacy model (en_core_web_sm, for instance). The second script is related to the automatic building of a knowledge base of regulatory events.

In order tu run the python scripts hosted in this repository, please follow the next steps:

1. Install spaCy as you can see in: https://spacy.io/usage#quickstart.
Be sure of having Python 3.9 in your system. We recomend to use a virtual environment as the spacy's installation instructions describes.

2. Set the PYTHONPATH variable in order to point to the sources of this project. For instance:
export PYTHONPATH=$PYTHONPATH:$HOME/bio_ner_tagger/src

3. Change directory to the bio_ner_tagger folder.

4. To set the training and evaluation examples, and the fine-tuning configuration file, proceed as follows:
python src/tagger/setter.py --model=en_core_web_sm --corpus=data/corpus_sars_cov --components_to_update=ner,tagger --config_output_path=./config_ner.cfg

5. The steps above define the files train.spacy and dev.spacy, and the config_ner.cfg configuration file. In order to fine-tune a model, please run: python -m spacy train ./config_ner.cfg --output ./model --paths.train ./dev.spacy --paths.dev ./dev.spacy

6. The step above builds a new fine-tuned model in the ./model folder. You can use that model to build the knowledge base, as you can see in the following line:
python src/tagger/kb_constructor.py --model=model/model-best --corpus=data/corpus_sars_cov

7. The output of the step above are two files: kbase.pl and kbase.text, available in the data/knowledge_base folder.

This repo offers two small sets of sentences to play with: the corpus_sars_cov and the corpus_covid. Both of them avalilable in the ./data projects's folder.





