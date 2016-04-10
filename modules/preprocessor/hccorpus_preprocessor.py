#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""**HC Corpus Preprocessor which inherits from BasePreprocessor.**"""

import sys
import unicodedata
import regex as re
from collections import defaultdict
from base_preprocessor import BasePreprocessor
from nltk.tokenize import sent_tokenize


class HcCorpusPreprocessor(BasePreprocessor):
    """
    **Hc-Corpus Preprocessor which preprocesses the Hc-Corpus.**

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
        """**Constructor which initializes the BasePreprocessor constructor.**"""
        self.language = language
        # If language is not specified, regex pattern for split is default ''
        self.lang_split_sent = defaultdict(lambda : u'')
        # Specify language specific split regex pattern
        lang_split_sent = [
            ('hindi', u'[।]'),
        ]
        # Store language specific regex pattern in the defaultdict
        for k,v in lang_split_sent:
            self.lang_split_sent[k] = v
        super(HcCorpusPreprocessor, self).__init__(
            corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=need_preprocessing,
            limit=limit
        )

    def _extract_corpus_data(self, data):
        """**Extract 4th column of corpus which contains the body.**"""
        line_split_list = data.split('\n')
        corpus_data = []
        for i in range(len(line_split_list)):
            tab_split_list = line_split_list[i].split('\t')
            for j in range(len(tab_split_list)):
                if j % 4 == 0 and j != 0:
                    corpus_data.append(tab_split_list[j].strip())
        return ". ".join(corpus_data)

    def _clean_word(self, word):
        """
        **Preprocess words after tokenizing words from sentences.**

        - Remove apostrophes ['s, s'].
        - Bring to lowercase.
        - Remove punctuations.
        - Remove English words from Non-English corpus data.
        """
        if self.language is "english":
            regex = ur"((\p{P}+)|(\p{S}+)|([0-9]+))"
        else:
            regex = ur"((\p{P}+)|(\p{S}+)|([0-9]+)|([A-Za-z]))"
        return re.sub(
            pattern=regex,
            repl='',
            string=word.lower()
        ).strip()

    def _tokenize_sentences(self, data):
        """
        **Sentence tokenize corpus.**

        - Sentence Tokenize the corpus using NLTK.
        - Remove punctuations [ except space ] from each individual sentences.

        .. seealso::
            * :mod:`nltk.tokenizers`
        """
        lang_specific_split_pattern = self.lang_split_sent[self.language]
        for generic_sentence_split in sent_tokenize(data):
            for sentence in re.split(
                lang_specific_split_pattern, generic_sentence_split
            ):
                clean_sentence = sentence.expandtabs().strip()
                if len(clean_sentence) > 0:
                    yield clean_sentence

    def _tokenize_words(self, sentence):
        """**Tokenize Words from sentences.**"""
        return sentence.split()

BasePreprocessor.register(HcCorpusPreprocessor)
