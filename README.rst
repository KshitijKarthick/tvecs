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


Install as a Package
~~~~~~~~~~~~~~~~~~~~

::

    # Install package
    sudo python setup.py install

    # Usage from cmd line without recommendations menu
    tvecs -c ./config.json

    # Usage from cmd line with recommendations menu
    tvecs -c ./config.json -r

    # Usage without config file, with models, without recommendations menu
    tvecs -l1 english -l2 hindi -m1 ./data/models/t-vex-english-models -m2 ./data/models/t-vex-hindi-models

    # Usage without config file, with models, with recommendations menu
    tvecs -r -l1 english -l2 hindi -m1 ./data/models/t-vex-english-models -m2 ./data/models/t-vex-hindi-models

    # Usage from python
    import tvecs.vector_space_mapper.vector_space_mapper as vm



Generate Documentation
~~~~~~~~~~~~~~~~~~~~~~

::

    # Generate HTML Documentation
    make html
    cd documentation/html && python -m SimpleHTTPServer
    # [ Open browser to localhost:8000 for visualization ]

    # Generate Man Pages
    make man
    cd documentation/man && man -l t-vecs.1


    # Other Makefile options
    make

    Please use `make <target>' where <target> is one of
    html       to make standalone HTML files
    dirhtml    to make HTML files named index.html in directories
    singlehtml to make a single large HTML file
    pickle     to make pickle files
    json       to make JSON files
    htmlhelp   to make HTML files and a HTML help project
    qthelp     to make HTML files and a qthelp project
    applehelp  to make an Apple Help Book
    devhelp    to make HTML files and a Devhelp project
    epub       to make an epub
    epub3      to make an epub3
    latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
    latexpdf   to make LaTeX files and run them through pdflatex
    latexpdfja to make LaTeX files and run them through platex/dvipdfmx
    text       to make text files
    man        to make manual pages
    texinfo    to make Texinfo files
    info       to make Texinfo files and run them through makeinfo
    gettext    to make PO message catalogs
    changes    to make an overview of all changed/added/deprecated items
    xml        to make Docutils-native XML files
    pseudoxml  to make pseudoxml-XML files for display purposes
    linkcheck  to check all external links for integrity
    doctest    to run all doctests embedded in the documentation (if enabled)
    coverage   to run coverage check of the documentation (if enabled)



Data
~~~~

Corpus Download details
'''''''''''''''''''''''

We are focusing on [English, Hindi]
other possible prospects we could look into Kannada, Tamil languages

Sources
    - HcCorpora http://www.corpora.heliohost.org/download.html
    - Emille Corpora http://www.emille.lancs.ac.uk/
    - Leipzig Corpora http://corpora.uni-leipzig.de/


Bilingual Dictionary details
''''''''''''''''''''''''''''

Provided in the repository, data/bilingual_dictionary.
Compiled using the following sources.

Credits
    - Shabdakosh http://www.shabdkosh.com/content/category/downloads/
    - Dicts Corpora http://dicts.info/dictlist1.php?l=Hindi


Evaluation Dataset details
''''''''''''''''''''''''''

Human relatedness judgement score datasets provided in data/evaluate

Credits
    - wordsim_relatedness_goldstandard
    - MEN_dataset_natural_form_full
    - Mturk_287
    - Mturk_771


Ensure Model is downloaded and extracted in the t-vex directory
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

-  data/corpus -> corpus
-  data/models -> models

Execution
~~~~~~~~~

::

    # Preprocessing, Model Generation, Bilingual Generation, Vector Space Mapping between two languages english hindi from the corpus using the config file

    python -im tvecs -c config.json

    # [ utilise the dictionary tvex_calls which contains results of every step performed ]

    # Bilingual generation, Vector space mapping between two languages english hindi providing the models

    python -im tvecs -l1 english -l2 hindi -m1 ./data/models/t-vex-english-model -m2 ./data/models/t-vex-hindi-model

    python -im tvecs -c config.json

    # [ utilise the dictionary tvex_calls which contains results of every step performed ]

Usage Details
~~~~~~~~~~~~~

T-Vecs Driver Module Cmd Line Args
''''''''''''''''''''''''''''''''''

::

    $ python -m tvecs --help

    usage: __main__.py [-h] [-v] [-s] [-i ITER] [-m1 MODEL1] [-m2 MODEL2]
                   [-l1 LANGUAGE1] [-l2 LANGUAGE2] [-c CONFIG]
                   [-b BILINGUAL_DICT] [-r]

    Script used to generate models

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -s, --silent          silence all logging
      -i ITER, --iter ITER  number of Word2Vec iterations
      -m1 MODEL1, --model1 MODEL1
                            pre-computed model file path
      -m2 MODEL2, --model2 MODEL2
                            pre-computed model file path
      -l1 LANGUAGE1, --language1 LANGUAGE1
                            language name of model 1/ text 1
      -l2 LANGUAGE2, --l2 LANGUAGE2
                            language name of model 2/ text 2
      -c CONFIG, --config CONFIG
                            config file path
      -b BILINGUAL_DICT, --bilingual BILINGUAL_DICT
                            bilingual dictionary path
      -r, --recommendations
                            provide recommendations


Config File Format
''''''''''''''''''

- See config.json in the repository for example.



Visualisation of vector space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    python -m tvecs.visualization.server
    [ Open browser to localhost:5000 for visualization ]
    [ Ensure model generation is completed before running visualization ]

Execution of Individual Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # bilingual dictionary generation -> clustering vectors from trained model
    python -m tvecs.bilingual_generator.clustering

    # model generation
    python -m tvecs.model_generator.model_generation

    # vector space mapping [ utilise the object vm to obtain recommendations
    python -m tvecs.vector_space_mapper.vector_space_mapper

Execution of Unit Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Run all unit tests
    py.test

    # Run individual module tests seperately
    py.test tests/test_emille_preprocessor.py
    py.test tests/test_leipzig_preprocessor.py
    py.test tests/test_hccorpus_preprocessor.py
