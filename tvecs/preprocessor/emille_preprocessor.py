#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""EMILLE Corpus Preprocessor which inherits from BasePreprocessor."""
import regex as re
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import sent_tokenize

from tvecs.preprocessor.base_preprocessor import BasePreprocessor
from tvecs.logger import init_logger as log

LOGGER = log.initialise('TVecs.Preprocessor')


class EmilleCorpusPreprocessor(BasePreprocessor):
    """
    Emille Corpus Preprocessor which preprocesses the EMILLE Corpus.

    API Documentation:
        :param corpus_fname: Corpus Filename to be preprocessed
        :param corpus_dir_path: Corpus Directory Path
                                [ Default Current Directory ]
        :param encoding: Encoding format of the corpus
                                [ Default utf-8 ]
        :param language: Language of the model constructed
                                [ Default English ]
        :param limit: Number of tokenized words to be limited to
                                [ Default None ]
        :param need_preprocessing: Preprocess corpus to obtain
            only the valid content from the file to an intermediate file
            [ False - Corpus has each sentence in seperate lines ]
        :type corpus_fname: :class:`String`
        :type corpus_dir_path: :class:`String`
        :type encoding: :class:`String`
        :type language: :class:`String`
        :type limit: :class:`Integer`
        :type need_preprocessing: :class:`Boolean`

    Private Methods
        .. automethod:: _extract_corpus_data
        .. automethod:: _clean_word
        .. automethod:: _tokenize_sentences
        .. automethod:: _tokenize_words


    .. seealso::
        * :class:`tvecs.preprocessor.base_preprocessor.BasePreprocessor`
    """

    def __init__(
        self,
        corpus_fname,
        corpus_dir_path='.',
        encoding='utf-8',
        language='english',
        need_preprocessing=False,
        limit=None
    ):
        """Constructor which initializes the BasePreprocessor constructor."""
        try:
            self.logger = LOGGER
        except NameError:
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
        self.logger.info('EmilleCorpusPreprocessor utilised')
        super(EmilleCorpusPreprocessor, self).__init__(
            corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=need_preprocessing,
            limit=limit
        )

    def _extract_corpus_data(self, data):
        """Extract contents of the 'p' tags which contain the body."""
        soup = BeautifulSoup(data, "html5lib")
        ptags = soup.find_all('p')
        content = []
        for index in range(len(ptags)):
            content.append(". ".join(list(ptags[index].strings)))
        return ". ".join(content)

    def _clean_word(self, word):
        """
        Preprocess words after tokenizing words from sentences.

        - Remove punctuations.
        - Remove English words from Non-English corpus data.
        """
        if self.language is "english":
            regex = r"((\p{P}+)|(\p{S}+)|([0-9]+))"
        else:
            regex = r"((\p{P}+)|(\p{S}+)|([0-9]+)|([A-Za-z]))"
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
        Sentence tokenize corpus.

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
        """Tokenize Words from sentences."""
        return sentence.split()

BasePreprocessor.register(EmilleCorpusPreprocessor)

if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
