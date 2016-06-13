.. T-Vecs documentation master file, created by
   sphinx-quickstart on Thu Apr  7 14:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://travis-ci.org/KshitijKarthick/tvecs.svg?branch=master
    :target: https://travis-ci.org/KshitijKarthick/tvecs
    :align: right

Welcome to T-Vecs's documentation!
==================================

The main documentation for the site is organized into a couple sections:


.. _user-docs:

	.. toctree::
		:maxdepth: 2
		:caption: Usage Documentation

	   	README



.. _dev-docs:

	.. toctree::
		:titlesonly:
		:caption: Development Documentation
		
		_dev_docs/modules



.. _test-docs:

	.. toctree::
		:caption: Testing Documentation
		
		_test_docs/modules



.. _dev-seq-diagr:

   	.. toctree::
   		:caption: Sequence Diagrams



	.. seqdiag::
		:align: center
   		:desctable:
   		:caption: Sequence Diagram for T-Vecs Driver Module

		seqdiag {
			t-vecs  -> preprocessor [label = "Preprocess English Corpus"];
			t-vecs <-- preprocessor [label = "Preprocessed English Corpus"];
			t-vecs  -> preprocessor [label = "Preprocess Hindi Corpus"];
			t-vecs <-- preprocessor [label = "Preprocessed Hindi Corpus"];
			t-vecs -> model_generator [label = "Construct Model for English"];
			t-vecs <-- model_generator [label = "English Model"]
			t-vecs -> model_generator [label = "Construct Model for Hindi"];
			t-vecs <-- model_generator [label = "Hindi Model"]
			t-vecs -> bilingual_generator [label = "Generate Bilingual Dictionary for English, Hindi"]
			t-vecs <-- bilingual_generator [label = "Bilingual Dictionary"]
			t-vecs -> vector_space_mapper [label = "English Model"];
			t-vecs -> vector_space_mapper [label = "Hindi Model"];
			t-vecs -> vector_space_mapper [label = "Bilingual Dictionary"];
			t-vecs <-- vector_space_mapper [label = "Mapping of English & Hindi Vector Spaces"];
		    t-vecs [description = "Driver Module"];
		    preprocessor [description = "Preprocessor for Corpus"];
	        model_generator [description = "Word2Vec implementation to Generate Semantic Word Embeddings"];
	        bilingual_generator [description = "Generates Bilingual Dictionary"];
	        vector_space_mapper [description = "Maps Vector Spaces between 2 Models using a Bilingual Dictionary"];
		}



	.. seqdiag::
		:align: center
   		:desctable:
   		:caption: Sequence Diagram for Visualization Recommendations

		seqdiag {
			client  -> server [label = "GET /index.html"];
			client <-- server [label = "Visualization Demo"];
			client  -> server [label = "GET /cross_lingual.html"];
			client <-- server [label = "Cross Lingual Demo"];
			client  -> server [label = "GET /get_cross_lingual_recommendations => lang1, lang2 & word sent"];
			server  -> vector_space_mapper [label = "Request for cross lingual Recommendations"];
			server <-- vector_space_mapper [label = "Cross Lingual Recommendations"];
			client <-- server [label = "JSON Response => Cross-lingual Recommendations"];
			client  -> server [label = "GET /retrieve_recommendations => language & word sent"];
			server  -> server [label = "Load Word2Vec Model & Obtain recommendations"];
			client <-- server [label = "JSON Response => Intra-lingual Recommendations"];

		    client [description = "HTTP Client"];
		    server [description = "CherryPy Server"];
	        vector_space_mapper [description = "Maps Vector Spaces between 2 Models using a Bilingual Dictionary"];
		}

	.. seqdiag::
		:align: center
   		:desctable:
   		:caption: Sequence Diagram for Visualization for Distances & Multivariate Analysis

		seqdiag {
			client  -> server [label = "GET /index.html"];
			client <-- server [label = "Visualization Demo"];
			client  -> server [label = "GET /distances.html"];
			client <-- server [label = "Semantic Word Distances"];
			client  -> server [label = "GET /get_distance => lang1, lang2, word1 & word2 sent"];
			server  -> vector_space_mapper [label = "Request for cosine similarity"];
			server <-- vector_space_mapper [label = "Cosine similarity b/w words"];
			client <-- server [label = "JSON Response => Distance b/w words"];
			client  -> server [label = "GET /multivariate_analysis.html"];
			client <-- server [label = "Multivariate Analysis Visualization"];
		    client [description = "HTTP Client"];
		    server [description = "CherryPy Server"];
	        vector_space_mapper [description = "Maps Vector Spaces between 2 Models using a Bilingual Dictionary"];
		}



	.. seqdiag::
		:align: center
   		:desctable:
   		:caption: Sequence Diagram for Preprocessor

		seqdiag {
			t-vecs  -> preprocessor [label = "Invoke Preprocessor\n with corpus"];
			preprocessor -> preprocessor [label = "_extract_corpus_data()"];
			preprocessor -> preprocessor [label = "_save_preprocessed_data()"];
			preprocessor -> preprocessor [label = "_tokenize_sentences()"];
			t-vecs <-- preprocessor [label = "Intermediate preprocessed\n file generated"];
			t-vecs  -> preprocessor [label = "get_preprocessed_text()"];
			preprocessor -> preprocessor [label = "_tokenized_words()"];
			preprocessor -> preprocessor [label = "_clean_word()"];
			t-vecs <-- preprocessor [label = "Return a list of sentences with tokenized words"];

		    t-vecs [description = "Driver Module"];
		    preprocessor [description = "Preprocessor for Corpus"];
		}



.. _dev-inh-diagr:

   	.. toctree::
   		:caption: Inheritance Diagrams

	.. inheritance-diagram:: tvecs.preprocessor.base_preprocessor.BasePreprocessor  tvecs.preprocessor.hccorpus_preprocessor.HcCorpusPreprocessor tvecs.preprocessor.leipzig_preprocessor.LeipzigPreprocessor tvecs.preprocessor.emille_preprocessor.EmilleCorpusPreprocessor
   		:parts: 1

.. _dev-experimental-results:

	.. toctree::
		:caption: Experimental Results

	+---------------+------------------+-------------------+--------------------+------------+
	| Corpus Size   | Bilingual Size   | Wordsim Dataset   | Correlation Score  | P-Value    |
	+===============+==================+===================+====================+============+
	| 136772323     | 11291            | MTurk-287         | 0.6268             | 1.83e-29   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 136772323     | 9032             | MTurk-287         | 0.6251             | 2.85e-29   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 136772323     | 4516             | MTurk-287         | 0.6130             | 6.50e-28   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 82063393      | 11291            | MTurk-287         | 0.6196             | 1.21e-28   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 82063393      | 6774             | MTurk-287         | 0.6195             | 1.22e-28   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 54708929      | 11291            | MTurk-287         | 0.5725             | 1.94e-23   |
	+---------------+------------------+-------------------+--------------------+------------+
	| 54708929      | 4516             | MTurk-287         | 0.5579             | 4.17e-22   |
	+---------------+------------------+-------------------+--------------------+------------+


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
