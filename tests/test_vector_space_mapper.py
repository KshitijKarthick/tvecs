#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Unit Test Cases for :mod:`tvecs.vector_space_mapper.vector_space_mapper`."""

import os
import pytest
import random

from tvecs.model_generator import model_generator as mod
from tvecs.bilingual_generator import bilingual_generator as bg
from tvecs.vector_space_mapper.vector_space_mapper import VectorSpaceMapper


class TestVectorSpaceMapper:
    """
    Unit Testing for module :mod:`tvecs.vector_space_mapper.vector_space_mapper`.

    Test Cases considered for the following functions
        - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.extract_vectors_and_words`
        - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_word`
        - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_vec`
        - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`
        - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`

    .. seealso::
        * :mod:`tvecs.vector_space_mapper.vector_space_mapper`
        * :mod:`pytest`
        * :mod:`tvecs.model_generator.model_generator`
    """

    def setup_class(cls):
        """
        Used to create a :mod:`tvecs.vector_space_mapper.vector_space_mapper`.

        - Learns transformation between two models
            - :mod:`tvecs.model_generator.model_generator`
            - :mod:`tvecs.model_generator.model_generator`
        """
        try:
            model_1 = mod.generate_model(
                language='english',
                corpus_fname='test_english',
                corpus_dir_path=os.path.join('tests', 'resources'),
                output_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True,
                output_fname='model_1'
            )
            model_2 = mod.generate_model(
                language='hindi',
                corpus_fname='test_hindi',
                corpus_dir_path=os.path.join('tests', 'resources'),
                output_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True,
                output_fname='model_2'
            )
        except Exception as err:
            pytest.fail(
                'Model construction failed: %s' % err.message
            )
        try:
            bilingual_dict = bg.load_bilingual_dictionary(
                os.path.join(
                    'data', 'bilingual_dictionary', 'english_hindi_train_bd'
                )
            )
        except Exception as err:
            pytest.fail(
                'Bilingual Dictionary Construction failed: %s' % err.message
            )
        try:
                cls.testing_obj = VectorSpaceMapper(model_1, model_2, bilingual_dict)
                cls.testing_obj.map_vector_spaces()
        except BaseException as err:
            pytest.fail(
                'Vector Space Mapping failed : %s' % err.message
            )

    def teardown_class(cls):
        """Delete models after construction."""
        try:
            os.remove(
                os.path.join('tests', 'resources', 'model_1')
            )
            os.remove(
                os.path.join('tests', 'resources', 'model_2')
            )
        except (OSError, IOError):
            pass

    def test_english_extract_vectors_and_words(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._extract_vectors_and_words`.

        Verify the data structure for the response of the function for English model.
        """
        obj = self.__class__.testing_obj
        expected_list = {
            u'has': (100,),
            u'have': (100,),
            u'\u0915\u093e': None
        }
        result_vec, result_word = obj._extract_vectors_and_words(
            obj.model_1, expected_list.keys()
        )
        temp_list = []
        for vec in result_vec:
            if vec is not None:
                vec = vec.shape
            temp_list.append(vec)

        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, "_extract_vectors_and_words failed for english model [ Data Structure test ]"

    def test_hindi_extract_vectors_and_words(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._extract_vectors_and_words`.

        Verify the data structure for the response of the function for Hindi model.
        """
        obj = self.__class__.testing_obj
        expected_list = {
            u'\u0915\u093e': (100,),
            u'\u0925\u0940': (100,),
            u'english': None
        }
        result_vec, result_word = obj._extract_vectors_and_words(
            obj.model_2, expected_list.keys()
        )
        temp_list = []
        for vec in result_vec:
            if vec is not None:
                vec = vec.shape
            temp_list.append(vec)

        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, "_extract_vectors_and_words failed for hindi model [ Data Structure test ]"

    def test_predict_vec_from_word(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_word`.

         Verify the data structure for the response of the function given a word.
        """
        obj = self.__class__.testing_obj
        expected = (100,)
        result = obj._predict_vec_from_word('has').shape
        assert expected == result, "_predict_vec_from_word execution failed [ Data Structure test ]"

    def test_predict_vec_from_vec(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_vec`.

        Verify the data structure for the response of the function given a vector.
        """
        obj = self.__class__.testing_obj
        expected_shape = (100,)
        result_shape = obj._predict_vec_from_vec(
            obj.model_1['has']
        ).shape
        assert expected_shape == result_shape, "_predict_vec_from_vec failed [ Data Structure test ]"

    def test_predict_vec_from_word_and_vec_match(self):
        """
        Test following functions.

         - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_vec`.
         - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_word`.

        Verify both functions provide same predictions.
        """
        obj = self.__class__.testing_obj
        result = obj._predict_vec_from_vec(
            obj.model_1['has']
        )
        expected = obj._predict_vec_from_word('has')

        assert all(result == expected), "Recommendations from _predict_vec_from_vec "\
            "and _predict_vec_from_word do not match"

    def test_num_recom_from_get_recommendations_from_word(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`.

        Verify number of recommendations conform to the number of recommendations requested.
        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_word('has', topn=num_recommendations)
        assert len(result) == num_recommendations, "_get_recommendations_from_word returned"\
            "wrong number of recommendations"

    def test_num_recom_from_get_recommendations_from_vec(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`.

        Verify number of recommendations conform to the number of recommendations requested.
        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_vec(obj.model_1['has'], topn=num_recommendations)
        assert len(result) == num_recommendations, "_get_recommendations_from_word returned"\
            "wrong number of recommendations"

    def test_get_recommendations_from_word(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`.

        Verify the response type from the function.
        """
        obj = self.__class__.testing_obj
        result = obj.get_recommendations_from_word('has')
        word_type, dist_type = (unicode, float)
        for word, dist in result:
            assert type(word) is word_type and type(dist) is dist_type, "_get_recommendations_from_word"\
                "returned wrong type"

    def test_get_recommendations_from_vec(self):
        """
        Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`.

        Verify the response type from the function.
        """
        obj = self.__class__.testing_obj
        result = obj.get_recommendations_from_vec(obj.model_1['has'])
        word_type, dist_type = (unicode, float)
        for word, dist in result:
            assert type(word) is word_type and type(dist) is dist_type, "_get_recommendations_from_word"\
                "returned wrong type"

    def test_get_recommendations_from_vec_and_word_match(self):
        """
        Test following functions.

         - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`
         - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`

        Verify the results from both functions match.
        """
        obj = self.__class__.testing_obj
        result = dict(obj.get_recommendations_from_word('has'))
        expected = dict(obj.get_recommendations_from_vec(obj.model_1['has']))
        for word, dist in expected.items():
            assert dist == result[word], "_get_recommendations_from_vec do not match"\
                "_get_recommendations_from_word"
