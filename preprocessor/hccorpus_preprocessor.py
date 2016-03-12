"""HC Corpus Preprocessor which inherits from BasePreprocessor."""

import sys
import regex as re
import unicodedata
from base_preprocessor import BasePreprocessor
from nltk.tokenize import sent_tokenize


class HcCorpusPreprocessor(BasePreprocessor):
    """Hc-Corpus Preprocessor which preprocesses the Hc-Corpus."""

    def __init__(
        self,
        corpus_fname,
        corpus_dir_path='.',
        encoding='utf-8',
        need_preprocessing=False
    ):
        """Constructor which initializes the BasePreprocessor constructor."""
        super(HcCorpusPreprocessor, self).__init__(
            corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=need_preprocessing
        )

    def _extract_corpus_data(self, data):
        """Extract 4th column of corpus which contains the body."""
        tab_split_list = data.split('\t')
        return ". ".join(
            tab_split_list[x] for x in range(
                len(tab_split_list)
            ) if x % 4 == 0 and x != 0
        )

    def _clean_word(self, word):
        """
        Preprocess words after tokenizing words from sentences.

        * Remove apostrophes ['s, s'].
        * Remove website urls [wordpress.com, blogspot.com].
        * Bring to lowercase.
        * Remove punctuations.
        """
        return re.sub(
            pattern=ur"(([a-zA-Z0-9]*).(com|net|org|in).?)|(\p{P}+)",
            repl='',
            string=word.lower().strip()
        )

    def _tokenize_sentences(self, data):
        """
        Sentence tokenize corpus.

        * Sentence Tokenize the corpus using NLTK.
        * Remove punctuations [ except space ] from each individual sentences.
        """
        # tbl = dict.fromkeys(
        #     i for i in xrange(sys.maxunicode)
        #     if unicodedata.category(unichr(i)).startswith('P')
        # )
        # return (
        #     sentence.translate(tbl) for sentence in sent_tokenize(data)
        # )
        return (
            sentence for sentence in sent_tokenize(data)
        )

    def _tokenize_words(self, sentence):
        """Tokenize Words from sentences."""
        return sentence.split()

BasePreprocessor.register(HcCorpusPreprocessor)
