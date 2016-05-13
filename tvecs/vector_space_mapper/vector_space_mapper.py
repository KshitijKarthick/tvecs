#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to map two Vector Spaces using a bilingual dictionary."""
import os
import codecs
import logging
from gensim.models import Word2Vec
import scipy.spatial.distance as dist
from sklearn.linear_model import RidgeCV
from sklearn import metrics

from tvecs.bilingual_generator import bilingual_generator as bg
from tvecs.logger import init_logger as log

LOGGER = log.initialise('TVecs.VectorSpaceMapper')


class VectorSpaceMapper(object):
    """
    Class to map two vector spaces together.

    - Vector spaces obtained using the two Word2Vec models.
    - Bilingual Dict used to map semantic embeddings between vector spaces.
    - Linear Regression utilised for the mapping from
        :mod:`sklearn.linear_model`

    API Documentation:
        :param model_1: Model constructed from Language 1 built using
            :mod:`tvecs.model_generator.model_generator`.
        :param model_2: Model constructed from Language 2 built using
            :mod:`tvecs.model_generator.model_generator`.
        :param bilingual_dict: Bilingual Dictionary for Language 1, Language 2.
        :param encoding: Encoding utilised in the corpora
        :type encoding: :mod:`String`
        :type model_1: :mod:`gensim.models.Word2Vec`
        :type model_2: :mod:`gensim.models.Word2Vec`
        :type bilingual_dict: :class:`List[(lang1, lang2), (lang1, lang2)]`

    .. seealso::
        * :mod:`tvecs.model_generator.model_generator`
        * :mod:`gensim.models.Word2Vec`
        * :mod:`sklearn.linear_model`
        * :mod:`scipy.spatial.distance`

    """

    def __init__(self, model_1, model_2, bilingual_dict, encoding='utf-8'):
        """Constructor initialization for the vector space mapper."""
        try:
            self.logger = LOGGER
        except NameError:
            self.logger = log.initialise('T-Vecs.VectorSpaceMapper')
        self.model_1 = model_1
        self.model_2 = model_2
        self.encoding = encoding
        self.lt = None
        self.bilingual_dict = bilingual_dict
        bilingual_dict = dict(bilingual_dict)
        self.logger.debug('Extracting vocabulary and vector list from model 1')
        self.vector_1_list, self.word_1_list = self._extract_vectors_and_words(
            self.model_1, bilingual_dict.keys()
        )
        self.logger.debug('Extracting vocabulary and vector list from model 2')
        (
            self.vector_2_list, self.word_2_list
        ) = VectorSpaceMapper._extract_vectors_and_words(
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

    @staticmethod
    def _extract_vectors_and_words(model, word_list):
        """Extract vocabulary and vectors from model from word list."""
        vector_list = []
        for word in word_list:
            try:
                vec = model[word]
            except KeyError:
                vec = None
            vector_list.append(vec)
        return vector_list, word_list

    def map_vector_spaces(self):
        """
        Perform linear regression upon the semantic embeddings.

        - Semantic embeddings obtained from vector space of corresponding
            bilingual words of the same language.
        """
        self.logger.info('Learning transformation between Vector Spaces.')
        self.lt = RidgeCV()
        self.lt.fit(self.vector_1_list, self.vector_2_list)

    def _predict_vec_from_word(self, word):
        return self._predict_vec_from_vec(self.model_1[word])

    def _predict_vec_from_vec(self, vector):
        return self.lt.predict(vector.reshape(1, -1))[0]

    def get_recommendations_from_vec(self, vector, topn=10):
        """
        Get topn most similar words from model-2 [language 2].

        - Vector for the word in Model 1 [Language 1] should be provided

        API Documentation:
            :param vector: Input a vector from Model 1,
                recommendations provided from Model 2.
            :param topn: Number of recommendations to be provided.
            :type vector: :class:`List`, :class:`numpy.array`
            :type topn: :class:`Integer`
            :return: Topn recommendations from Model 2.
            :rtype: :class:`List`
        """
        if self.lt is not None:
            try:
                data = self.model_2.most_similar(
                    positive=[
                        self._predict_vec_from_vec(vector)
                    ],
                    topn=topn
                )
            except KeyError:
                data = None
        else:
            logging.error('First Map Vector Spaces')
            data = None
        return data

    def get_recommendations_from_word(self, word, topn=10, pretty_print=False):
        """
        Get topn most similar words from model-2 [language 2].

        - Word from Model 1 [Language 1] should be provided

        API Documentation:
            :param word: Input a word from Model 1,
                recommendations provided from Model 2.
            :param topn: Number of recommendations to be provided.
            :param pretty_print: Pretty Print the recommendations correctly.
            :type pretty_print: :class:`Boolean`
            :type word: String expected [ usually unicode preferred ]
            :type topn: :class:`Integer`
            :return: Topn recommendations from Model 2.
            :rtype: :class:`List`
        """
        try:
            word = word.decode(self.encoding)
        except UnicodeEncodeError:
            pass
        if self.lt is not None:
            try:
                data = self.model_2.most_similar(
                    positive=[
                        self._predict_vec_from_word(word)
                    ],
                    topn=topn
                )
            except KeyError:
                data = None
        else:
            logging.error('First Map Vector Spaces')
            data = None
        if pretty_print is True:
            print "\n%s\t=>\t%s\n" % ("Word", "Score")
            for prediction in data:
                print "%s\t=>\t%s" % (prediction[0], prediction[1])
            print "\n"
        return data

    def obtain_cosine_similarity(self, word_1, word_2):
        """
        Obtain cosine similarity.

        - Cosine Similarity between word_2 and predicted word using word_1

        API Documentation:
            :param word_1: Used to predict possible vector from Model 2
                using word from Model 1.
            :param word_2: Used for comparison in cosine similarity.
            :type word_1: :class:`String`
            :type word_2: :class:`String`
            :return: Cosine similarity between predicted word and actual word.
            :rtype: :class:`Float`
        """
        try:
            vec_1 = self._predict_vec_from_word(word_1)
            vec_2 = self.model_2[word_2]
            return 1 - dist.cosine(vec_1, vec_2)
        except KeyError:
            return None

    def obtain_mean_square_error_from_dataset(self, dataset_path, ):
        """
        Obtain Mean Square Error from bilingual dataset.

        API Documentation:
            :param dataset_path: Path for the test bilingual dictionary.
            :type dataset_path: :class:`String`
            :return: %% of reduction of Mean Square Error after transformation.
            :rtype: :class:`Float`
        """
        self.logger.info(
            'Obtain mean square error from dataset: %s', dataset_path
        )
        bilingual_dictionary = bg.load_bilingual_dictionary(dataset_path)
        avg = 0.0
        count = 0.0
        expected_with_tr = []
        actual_with_tr = []
        expected = []
        actual = []
        for tup in bilingual_dictionary:
            word_1 = tup[0]
            word_2 = tup[1]
            try:
                pr_vector_1 = self._predict_vec_from_word(word_1)
                vector_1 = self.model_1[word_1]
                vector_2 = self.model_2[word_2]
                expected.append(vector_1)
                actual.append(vector_2)
                expected_with_tr.append(pr_vector_1)
                actual_with_tr.append(vector_2)
            except KeyError:
                pass
        score = metrics.mean_squared_error(expected, actual)
        score_with_tr = metrics.mean_squared_error(
            expected_with_tr, actual_with_tr
        )
        self.logger.info(
            'Mean Square Error for Dataset without transformation: %s', score
        )
        self.logger.info(
            'Mean Square Error for Dataset'
            ' with transformation: %s', score_with_tr
        )
        error_reduction = ((score - score_with_tr) / score) * 100
        self.logger.info(
            'Reduction in Mean Square Error'
            ' with transformation: %s %%', error_reduction
        )
        return error_reduction


if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    model_1 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    model_2 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-hindi-model')
    )
    bilingual_dict = bg.load_bilingual_dictionary(
        os.path.join(
            'data', 'bilingual_dictionary', 'english_hindi_train_bd'
        )
    )
    vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
    vm.map_vector_spaces()
    LOGGER.info(
        'Evaluation of Testing Dataset'
    )
    vm.obtain_mean_square_error_from_dataset(dataset_path=os.path.join(
        'data', 'bilingual_dictionary', 'english_hindi_test_bd'
    ))
    LOGGER.info(
        'Evaluation of Training Dataset'
    )
    vm.obtain_mean_square_error_from_dataset(dataset_path=os.path.join(
        'data', 'bilingual_dictionary', 'english_hindi_train_bd'
    ))
