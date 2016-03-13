"""Module to map two Vector Spaces using a bilingual dictionary."""

import os
import logging
import codecs
from gensim.models import Word2Vec
from sklearn.linear_model import LinearRegression


class VectorSpaceMapper(object):
    """
    Class to Map two vector spaces together.

    Vector spaces obtained using the two Word2Vec models.
    Bilingual Dictionary used to map semantic embeddings between vector spaces.
    Linear Regression utilised for the mapping
    """

    def __init__(self, model_1, model_2, bilingual_dict):
        """Constructor initialization for the vector space mapper."""
        logging.basicConfig(level=logging.INFO)
        self.model_1 = model_1
        self.model_2 = model_2
        self.lt = None
        self.bilingual_dict = bilingual_dict
        bilingual_dict = dict(bilingual_dict)
        self.vector_1_list, self.word_1_list = self._extract_vectors_and_words(
            self.model_1, bilingual_dict.keys()
        )
        self.vector_2_list, self.word_2_list = self._extract_vectors_and_words(
            self.model_2, bilingual_dict.values()
        )
        # Remove corresponding elements if any vectors were missing from models
        # across both languages
        (self.vector_1_list, self.word_1_list, self.vector_2_list,
            self.word_2_list) = zip(*[
                (self.vector_1_list[index], self.word_1_list[index],
                    self.vector_2_list[index], self.word_2_list[index])
                for index in range(len(self.vector_1_list))
                if (
                    (self.vector_1_list[index] is not None) and (
                        self.vector_2_list[index] is not None)
                )
            ]
        )

    def _extract_vectors_and_words(self, model, word_list):
        vector_list = []
        for word in word_list:
            try:
                vec = model[word]
            except KeyError:
                vec = None
            vector_list.append(vec)
        return (vector_list, word_list)

    def map_vector_spaces(self):
        """
        Perform linear regression upon the semantic embeddings.

        Semantic embeddings obtained from vector space of corresponding
        bilingual words of the same language
        """
        self.lt = LinearRegression()
        self.lt.fit(self.vector_1_list, self.vector_2_list)

    def _predict_vec_from_word(self, word):
        return self._predict_vec_from_vec(self.model_1[word])[0]

    def _predict_vec_from_vec(self, vector):
        return self.lt.predict(vector)[0]

    def get_recommendations_from_vec(self, vector, topn=10):
        """
        Get topn most similar words from model-2 [language 2].

        vector for the word in model-1 [language 1] should be provided
        """
        if self.lt is not None:
            data = self.model_2.most_similar(
                positive=[
                    self._predict_vec_from_vec(vector)
                ],
                topn=topn
            )
        else:
            logging.error('First Map Vector Spaces')
            data = None
        return data

    def get_recommendations_from_word(self, word, topn=10):
        """
        Get topn most similar words from model-2 [language 2].

        word from model-1 [language 1] should be provided
        """
        if self.lt is not None:
            data = self.model_2.most_similar(
                positive=[
                    self._predict_vec_from_word(word)
                ],
                topn=topn
            )
        else:
            logging.error('First Map Vector Spaces')
            data = None
        return data

if __name__ == '__main__':

    model_1 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    model_2 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-hindi-model')
    )
    with codecs.open(
        os.path.join('data', 'bilingual_dictionary'), 'r', encoding='utf-8'
    ) as file:
        data = file.read().split('\n')
        bilingual_dict = [
            (line.split(' ')[0], line.split(' ')[1])
            for line in data
        ]
        vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
