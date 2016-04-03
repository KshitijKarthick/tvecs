#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Module used to specify abstract Preprocessor Class.

* BasePreprocessor is an Abstract Base Class
  with basic abstract preprocessor functionality.
"""

import os
import codecs
import logging
from abc import ABCMeta, abstractmethod
import fileinput


class BasePreprocessor(object):
    """Abstract Base Class with basic preprocessor functionality."""

    __metaclass__ = ABCMeta

    def __init__(
        self,
        corpus_fname,
        corpus_dir_path='.',
        encoding='utf-8',
        need_preprocessing=False,
        limit=None
    ):
        """
        Constructor initialization for BasePreprocessor.

        Function Parameters:
        * corpus_fname       - (string)  - Corpus Filename to be preprocessed
        * corpus_dir_path    - (string)  - Corpus Directory Path
                                           [ Default Current Directory ]
        * encoding           - (string)  - Encoding format of the corpus
                                           [ Default utf-8 ]
        * need_preprocessing - (boolean) - Preprocess corpus to obtain
                                           only the valid content from the file
                                           to an intermediate file
                                           [ False - Corpus has each sentence
                                            in seperate lines ]
        """
        logging.basicConfig(level=logging.INFO)
        self.limit = limit
        self.corpus_fname = corpus_fname
        self.corpus_path = os.path.join(
            corpus_dir_path, self.corpus_fname
        )
        self.encoding = encoding
        if need_preprocessing is True:
            logging.info('Preprocessing Corpus')
            self.preprocessed_corpus_path = os.path.join(
                corpus_dir_path, '%s.preprocessed' % (corpus_fname)
            )
            if os.path.exists(self.preprocessed_corpus_path) is False:
                with codecs.open(
                    self.corpus_path, 'r', encoding=self.encoding
                ) as file:
                    logging.info('Extracting Corpus Data')
                    self._save_preprocessed_data(
                        data=self._extract_corpus_data(
                            data=file.read()
                        ),
                        output_fpath=self.preprocessed_corpus_path
                    )
            else:
                logging.info('Preprocessed Corpus found')
            self.preprocessed_corpus_fname = '%s.preprocessed' % (corpus_fname)
        else:
            self.preprocessed_corpus_fname = self.corpus_fname
            self.preprocessed_corpus_path = os.path.join(
                corpus_dir_path,
                self.preprocessed_corpus_fname
            )

    def _save_preprocessed_data(self, data, output_fpath):
        """
        Save the extracted valid content.

        Extracted content tokenized into sentences and stored intermediate file

        Function Parameters:
        data         - (string)  - Extracted data
        output_fname - (string)  - Intermediate file path
                                   [ Inclusive of file name ]
        """
        with codecs.open(output_fpath, 'w', encoding=self.encoding) as file:
            logging.info("Tokenizing Corpus into Sentences")
            sentence_tokenized = self._tokenize_sentences(data)
            logging.info('Saving Preprocessed Corpus')
            sentence_tokenized = (
                '%s\n' % (sentence) for sentence in sentence_tokenized
            )
            file.writelines(sentence_tokenized)

    @abstractmethod
    def _extract_corpus_data(self, data):
        """
        Extract valid content from the Corpus.

        Executed only if need_preprocessing is set to True
        """
        raise NotImplementedError(
            "Base Class _extract_corpus_data() not implemented"
        )

    @abstractmethod
    def _clean_word(self, data):
        """
        After Tokenizing into words, function is called for individual word.

        Called by __iter__() which returns list of words.
        """
        raise NotImplementedError(
            "Base Class _clean_data() not implemented"
        )

    @abstractmethod
    def _tokenize_sentences(self, data):
        """Function to tokenize corpus data into sentences."""
        raise NotImplementedError(
            "Base Class _tokenize_sentences() not implemented"
        )

    @abstractmethod
    def _tokenize_words(self, sentence):
        """Function to tokenize sentences into words."""
        raise NotImplementedError(
            "Base Class _tokenize_words() not implemented"
        )

    def get_preprocessed_text(self, limit=None):
        """
        Generator generates preprocessed list of tokenized words on every call.

        * Read Sentence tokenized intermediate preprocessed file.
        * Tokenize and preprocess words, return list of words from a sentence.
        """
        count = 0
        if limit is None:
            limit = self.limit
        for sentence in fileinput.input(
            files=[self.preprocessed_corpus_path],
            openhook=fileinput.hook_encoded(self.encoding)
        ):
            word_list = (
                self._clean_word(
                    word
                ) for word in self._tokenize_words(sentence)
            )
            word_list = [
                word for word in word_list if len(word) is not 0
            ]
            count += len(word_list)
            if limit is not None and count >= limit:
                fileinput.close()
                raise StopIteration
            else:
                yield word_list

    def __iter__(self):
        """Iterator provided for get_preprocessed_text."""
        for tokenized_sentence in self.get_preprocessed_text():
            yield tokenized_sentence
