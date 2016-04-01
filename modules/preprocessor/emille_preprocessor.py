"""EMILLE Corpus Preprocessor which inherits from BasePreprocessor."""

import regex as re
from base_preprocessor import BasePreprocessor
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup


class EmilleCorpusPreprocessor(BasePreprocessor):
    """Emille Corpus Preprocessor which preprocesses the EMILLE Corpus."""

    def __init__(
        self,
        corpus_fname,
        corpus_dir_path='.',
        encoding='utf-8',
        need_preprocessing=False,
        limit=None
    ):
        """Constructor which initializes the BasePreprocessor constructor."""
        super(EmilleCorpusPreprocessor, self).__init__(
            corpus_fname,
            corpus_dir_path=corpus_dir_path,
            encoding=encoding,
            need_preprocessing=need_preprocessing,
            limit=limit
        )

    def _extract_corpus_data(self, data):
        """Extract contents of the 'p' tags which contain the body."""

        soup = BeautifulSoup(data)
        ptags = soup.find_all('p')
        content =[]
        for index in range(len(ptags)):
            content.append(ptags[index].string)
        return content

    def _clean_word(self, word):
        """
        Preprocess words after tokenizing words from sentences.
        * Remove punctuations.
        """
     
        # 
        return re.sub(
            pattern=ur"((\p{P}+)|(\p{S}))",
            repl='',
            string=word.lower()
        ).strip()

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

BasePreprocessor.register(EmilleCorpusPreprocessor)
