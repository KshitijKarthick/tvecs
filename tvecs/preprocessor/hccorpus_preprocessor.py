#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""HC Corpus Preprocessor which inherits from BasePreprocessor."""
import regex as re
from collections import defaultdict
from nltk.tokenize import sent_tokenize

from tvecs.preprocessor.base_preprocessor import BasePreprocessor
from tvecs.logger import init_logger as log

LOGGER = log.initialise('TVecs.Preprocessor')


class HcCorpusPreprocessor(BasePreprocessor):
    """
    Hc-Corpus Preprocessor which preprocesses the Hc-Corpus.

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
        need_preprocessing=False,
        language='english',
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
        self.logger.info('HcCorpusPreprocessor utilised')
        super(HcCorpusPreprocessor, self).__init__(
            corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=need_preprocessing,
            limit=limit
        )

    def _extract_corpus_data(self, data):
        """Extract 4th column of corpus which contains the body."""
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
        Preprocess words after tokenizing words from sentences.

        - Remove apostrophes ['s, s'].
        - Bring to lowercase.
        - Remove punctuations.
        - Remove English words from Non-English corpus data.
        """
        if self.language == "english":
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

BasePreprocessor.register(HcCorpusPreprocessor)

if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
