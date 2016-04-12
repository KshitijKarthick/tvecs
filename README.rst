T-Vecs
======

Setup Environment
~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/KshitijKarthick/t-vecs.git
    cd t-vecs
    pip install -r requirements.txt
    # Only Model needs to be downloaded and extracted in the t-vex directory

Prerequisites
~~~~~~~~~~~~~

-  Python 2.7 setup and installed
-  Pip setup and installed
-  Ensure all dependencies of requirements.txt are satisfied
-  Download nltk\_data using nltk.download() -> only tokenizers required
-  Download corpus and extract in specified directory

Download Corpus
~~~~~~~~~~~~~~~

Corpus Download details
'''''''''''''''''''''''

http://www.corpora.heliohost.org/download.html

| We are focusing on [English, Hindi]
| other possible prospects we could look into Kannada, Tamil languages

Ensure Model is downloaded and extracted in the t-vex directory
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

-  data/corpus -> corpus
-  data/models -> models

Execution
~~~~~~~~~

::

      # Preprocessing, Model Generation, Bilingual Generation, Vector Space Mapping between two languages english hindi from the corpus

        python2 -im t-vecs -l1 kannada -l2 tamil -t1 ./data/corpus/English/all.txt -t2 ./data/corpus/Hindi/all.txt
      # [ utilise the dictionary tvex_calls which contains results of every step performed ]

      # Bilingual generation, Vector space mapping between two languages english hindi providing the models

        python2 -im t-vecs -l1 english -l2 hindi -m1 ./data/models/t-vex-english-model -m2 ./data/models/t-vex-hindi-model
      # [ utilise the dictionary tvex_calls which contains results of every step performed ]

Usage Details
~~~~~~~~~~~~~

::

    $ python2 -m t-vecs --help

    usage: t-vecs.py [-h] [-v] [-s] [-i ITER] [-m1 MODEL1] [-m2 MODEL2] -l1
                     LANGUAGE1 -l2 LANGUAGE2 [-t1 CORPUS1] [-t2 CORPUS2]

    Script used to generate models

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -s, --silent          silence all logging
      -i ITER, --iter ITER  number of word2vec iter
      -m1 MODEL1, --model1 MODEL1
                            pre-computed model file path
      -m2 MODEL2, --model2 MODEL2
                            pre-computed model file path
      -l1 LANGUAGE1, --language1 LANGUAGE1
                            Language name of model 1/ text 1
      -l2 LANGUAGE2, --l2 LANGUAGE2
                            Language name of model 2/ text 2
      -t1 CORPUS1, --text1 CORPUS1
                            text corpus for model generation
      -t2 CORPUS2, --text2 CORPUS2
                            text corpus for model generation

Visualisation of vector space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    cd visualization
    python2 server.py
    [ Open browser to localhost:5000 for visualization ]
    [ Ensure model generation is completed before running visualization ]

Execution of Individual Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # bilingual dictionary generation -> clustering vectors from trained model
    python2 -m modules.bilingual_generator.clustering

    # model generation
    python2 -m modules.model_generator.model_generation

    # vector space mapping [ utilise the object vm to obtain recommendations
    python2 -m modules.vector_space_mapper.vector_space_mapper

Execution of Unit Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Run all unit tests
    py.test

    # Run individual module tests seperately
    py.test tests/test_emille_preprocessor.py
    py.test tests/test_leipzig_preprocessor.py
    py.test tests/test_hccorpus_preprocessor.py
