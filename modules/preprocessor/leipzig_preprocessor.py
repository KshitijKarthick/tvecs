#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Leipzig Preprocessor which inherits from BasePreprocessor."""

import codecs
import os
from collections import defaultdict

import regex as re

from base_preprocessor import BasePreprocessor
from modules.logger import init_logger as log


class LeipzigPreprocessor(BasePreprocessor):
    """
    Leipzig Preprocessor which preprocesses the Leipzig-Corpus.

    .. seealso::
        * :class:`modules.preprocessor.base_preprocessor.BasePreprocessor`
    """

    def __init__(
        self,
        corpus_fname,
        corpus_dir_path='.',
        encoding='utf-8',
        need_preprocessing=False,
        language='english',
        limit=None
    ):
        """Constructor which initializes the BasePreprocessor constructor."""
        self.logger = log.initialise('T-Vecs.Preprocessor')
        self.language = language
        # If language is not specified, regex pattern for split is default ''
        self.lang_split_sent = defaultdict(lambda: u'')
        # Specify language specific split regex pattern
        lang_split_sent = [
            ('hindi', u'[।]'),
        ]
        # Store language specific regex pattern in the defaultdict
        for k, v in lang_split_sent:
            self.lang_split_sent[k] = v
        self.logger.info('LeipzigPreprocessor utilised')
        preprocessed_corpus_fname = "%s.preprocessed" % corpus_fname
        if not os.path.exists(
            os.path.join(corpus_dir_path, preprocessed_corpus_fname)
        ):
            # < -- call function to preprocess leipzig corpus -- >
            self.leipzig_corpus_preprocess(
                corpus_fname, corpus_dir_path, encoding
            )

        # < -- call BasePreprocessor Constructor -- >
        super(LeipzigPreprocessor, self).__init__(
            corpus_fname=preprocessed_corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=False,
            limit=limit
        )

    def leipzig_corpus_preprocess(
            self,
            corpus_fname,
            corpus_dir_path,
            encoding
    ):
        """
        Extract valid content from the Corpus.

        - Store extracted corpus data in corpus_fname.preprocessed
        """
        self.logger.debug('Extracting Corpus data')
        with codecs.open(
            os.path.join(
                corpus_dir_path, corpus_fname
            ), 'r', encoding='utf-8'
        ) as file:
            line_split_list = file.read().split("\n")
            tab_split_list = [
                line.split('\t')[1] for line in line_split_list
                ]
            extracted_corpus = "\n".join(tab_split_list)
            with codecs.open(
                    os.path.join(
                        corpus_dir_path, '%s.preprocessed' % (corpus_fname)
                    ), 'w', encoding='utf-8'
            ) as extracted_corpus_file:
                extracted_corpus_file.write(extracted_corpus)

    def _extract_corpus_data(self, data):
        """
        Function not utilised for Leipzig Corpus.

        - Executed only if need_preprocessing is set to True
        """
        raise NotImplementedError(
            "Base Class _extract_corpus_data() not implemented"
        )

    def _clean_word(self, word):
        """
        Preprocess words after tokenizing words from sentences.

        - Remove apostrophes ['s, s'].
        - Bring to lowercase.
        - Remove punctuations.
        - Remove English words from Non-English corpus data.
        """
        if self.language is "english":
            regex = ur"((\p{P}+)|(\p{S}+)|([0-9]+))"
        else:
            regex = ur"((\p{P}+)|(\p{S}+)|([0-9]+)|([A-Za-z]))"
        # Handle Apostrophe's correctly you'll => you
        selected_word = re.match(pattern=u"(.*)['’].*?", string=word)
        # If selected word matches a word with apostrophe
        if selected_word is not None:
            word = selected_word.groups()[0]
        # Handle Pair words ice-cream => ice cream
        word = re.sub(pattern="-", repl=' ', string=word)
        return re.sub(
            pattern=regex,
            repl='',
            string=word.lower()
        ).strip().split()

    def _tokenize_sentences(self, data):
        """
        Function to tokenize corpus data into sentences.

        - Function not utilised for Leipzig Corpus

        .. seealso::
            * :mod:`nltk.tokenizers`
        """
        raise NotImplementedError(
            "Base Class _tokenize_sentences() not implemented"
        )

    def _tokenize_words(self, sentence):
        """Tokenize Words from sentences."""
        return sentence.split()

BasePreprocessor.register(LeipzigPreprocessor)
