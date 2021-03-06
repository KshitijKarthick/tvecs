#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Unit Test Cases for :mod:`tvecs.vector_space_mapper.vector_space_mapper`.

.. py:currentmodule:: tvecs.vector_space_mapper.vector_space_mapper
"""

import os
import pytest
import random

from tvecs.model_generator import model_generator as mod
from tvecs.bilingual_generator import bilingual_generator as bg
from tvecs.vector_space_mapper.vector_space_mapper import VectorSpaceMapper


class TestVectorSpaceMapper:
    """
    Unit Testing for :mod:`tvecs.vector_space_mapper.vector_space_mapper`.

    Test Cases considered for the following functions
        - :func:`VectorSpaceMapper.extract_vectors_and_words`
        - :func:`VectorSpaceMapper._predict_vec_from_word`
        - :func:`VectorSpaceMapper._predict_vec_from_vec`
        - :func:`VectorSpaceMapper.get_recommendations_from_vec`
        - :func:`VectorSpaceMapper.get_recommendations_from_word`

    .. seealso::
        * :mod:`tvecs.vector_space_mapper.vector_space_mapper`
        * :mod:`pytest`
        * :mod:`tvecs.model_generator.model_generator`
    """

    def setup_class(cls):
        """
        Setup Unit Testing for :class:`VectorSpaceMapper`.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 01
        |
        | *Description* : Create an instance of
        |                 :mod:`tvecs.vector_space_mapper.vector_space_mapper`.
        |
        | *Preconditions* : Corpus data for both languages
        |                   and bilingual dictionary exists.
        |
        | *Test Parameters* : model_1, model_2, bilingual_dict
        |
        | *Test Data* : model_1 = English, model_2 = Hindi, bilingual_dict =
        |               'data/bilingual_dictionary/english_hindi_train_bd'
        |
        | *Expected Result* : Vector Space Mapping created
        |
        | *Actual Result* : Vector Space Mapping created
        |
        | **Status : Pass**
        |

        - Learns transformation between two models
            - :mod:`tvecs.model_generator.model_generator`
            - :mod:`tvecs.model_generator.model_generator`
        """
        try:
            model_1 = mod.generate_model(
                preprocessor_type='HcCorpusPreprocessor',
                language='english',
                corpus_fname='test_english',
                corpus_dir_path=os.path.join('tests', 'resources'),
                output_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True,
                output_fname='model_1'
            )
            model_2 = mod.generate_model(
                preprocessor_type='HcCorpusPreprocessor',
                language='hindi',
                corpus_fname='test_hindi',
                corpus_dir_path=os.path.join('tests', 'resources'),
                output_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True,
                output_fname='model_2'
            )
        except Exception as err:
            pytest.fail(
                'Model construction failed: %s' % err
            )
        try:
            bilingual_dict = bg.load_bilingual_dictionary(
                os.path.join(
                    'data', 'bilingual_dictionary', 'english_hindi_train_bd'
                )
            )
        except Exception as err:
            pytest.fail(
                'Bilingual Dictionary Construction failed: %s' % err
            )
        try:
                cls.testing_obj = VectorSpaceMapper(
                    model_1, model_2, bilingual_dict
                )
                cls.testing_obj.map_vector_spaces()
        except BaseException as err:
            pytest.fail(
                'Vector Space Mapping failed : %s' % err
            )

    def teardown_class(cls):
        """
        Delete temp files generated for tests.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 02
        |
        | *Description* : Delete models after construction to remove
        |                 residual of setup_test [Test Case Number 01]
        |
        | *Preconditions* : model1 and model2 exist
        |
        | *Test Parameters* : model1 and model2 file paths
        |
        | *Test Data* :
        |   model1 file path = 'tests/resources/model1'
        |   model2 file path = 'tests/resources/model2'
        |
        | *Expected Result* : Models deleted
        |
        | *Actual Result* : Models deleted
        |
        | **Status : Pass**
        |

        """
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
        r"""
        Ensure valid data structure from extract_vectors_and_words for english.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 03
        |
        | *Description* : Verify the data structure for the
        |                 response of the function for English model.
        |                 Test
        |                 :func:`VectorSpaceMapper._extract_vectors_and_words`
        |
        | *Preconditions* : The English model exists
        |
        | *Test Parameters* : model_1 and expected_list[keys]
        |
        | *Test Data* : model_1 is English model, expected_list[keys] = {
        |                 u'has', u'have', u'\u0915\u093e'
        |               }
        |
        | *Expected Result* : Data structure consists of 1 vector
        |                 of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector
        |                 of 100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |

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
        assert_err_msg = "_extract_vectors_and_words failed for english" \
            " model [ Data Structure test ]"
        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, assert_err_msg

    def test_hindi_extract_vectors_and_words(self):
        r"""
        Ensure valid data structure from extract_vectors_and_words for hindi.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 04
        |
        | *Description* : Verify the data structure for the response of the
        |                 function for Hindi model.
        |                 Test
        |                 :func:`VectorSpaceMapper._extract_vectors_and_words`
        |
        | *Preconditions* : The Hindi model exists
        |
        |
        | *Test Parameters* : model_2 and expected_list[keys]
        |
        | *Test Data* : model_2 is Hindi model, expected_list[keys] = {
        |                   u'\u0915\u093e', u'\u0925\u0940', u'english'
        |               }
        |
        | *Expected Result* : Data structure consists of 1 vector
        |                  of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector
        |                  of 100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |


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
        assert_err_msg = "_extract_vectors_and_words failed for hindi" \
            " model [ Data Structure test ]"
        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, assert_err_msg

    def test_predict_vec_from_word(self):
        """
        Ensure valid data structure from predict_vec_from_word.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 05
        |
        | *Description* : Verify the data structure for the response of the
        |                 function given a word.
        |                 Test :func:`VectorSpaceMapper._predict_vec_from_word`
        |
        | *Preconditions* : English model exists
        |
        | *Test Parameters* : word passed to _predict_vec_from_word
        |
        | *Test Data* : word = u'has'
        |
        | *Expected Result* : Data structure consists of 1 vector of
        |                     100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of
        |                   100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |


        """
        obj = self.__class__.testing_obj
        expected = (100,)
        result = obj._predict_vec_from_word('has').shape
        assert_err_msg = "_predict_vec_from_word execution failed " \
            "[ Data Structure test ]"
        assert expected == result, assert_err_msg

    def test_predict_vec_from_vec(self):
        """
        Ensure valid data structure from predict_vec_from_vec.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 06
        |
        | *Description* : Verify the data structure for the response
        |                 of the function given a vector.
        |                 Test :func:`VectorSpaceMapper._predict_vec_from_vec`
        |
        | *Preconditions* : English model exists
        |
        | *Test Parameters* : vector passed to _predict_vec_from_vec
        |
        | *Test Data* : vector = obj.model_1['has']
        |
        | *Expected Result* : Data structure consists of 1 vector of
        |                     100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of
        |                   100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        expected_shape = (100,)
        result_shape = obj._predict_vec_from_vec(
            obj.model_1.wv['has']
        ).shape
        assert_err_msg = "_predict_vec_from_vec failed [ Data Structure test ]"
        assert expected_shape == result_shape, assert_err_msg

    def test_predict_vec_from_word_and_vec_match(self):
        """
        Validate output of predict_vec_from_word.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 07
        |
        | *Description* : Verify both functions provide same predictions.
        |                 Test following functions:
        |                    - :func:`VectorSpaceMapper._predict_vec_from_vec`
        |                    - :func:`VectorSpaceMapper._predict_vec_from_word`
        |
        | *Preconditions* : English model exists
        |
        | *Test Parameters* : vector passed to _predict_vec_from_vec,
        |                     word passed to _predict_vec_from_word
        |
        | *Test Data* : vector = obj.model_1['has'], word = 'has'
        |
        | *Expected Result* : Vector prediction matches
        |
        | *Actual Result* : Vector prediction matches
        |
        | **Status : Pass**
        |
        """
        obj = self.__class__.testing_obj
        result = obj._predict_vec_from_vec(
            obj.model_1.wv['has']
        )
        expected = obj._predict_vec_from_word('has')
        assert_err_msg = "Recommendations from _predict_vec_from_vec"\
            "and _predict_vec_from_word do not match"
        assert all(result == expected), assert_err_msg

    def test_num_recom_from_get_recommendations_from_word(self):
        """
        Validate num of recommendations from get_recommendations_from_word.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 08
        |
        | *Description* : Verify number of recommendations conform to the
        |               number of recommendations requested.
        |               Test
        |               :func:`VectorSpaceMapper.get_recommendations_from_word`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : num_recommendations
        |
        | *Test Data* : num_recommendations = random.randint(1,10)
        |
        | *Expected Result* : The number of recommendations returned is equal
        |                     to the number of recommendations requested.
        |
        | *Actual Result* : The number of recommendations returned is equal
        |                   to the number of recommendations requested.
        |
        | **Status : Pass**
        |
        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_word(
            'has', topn=num_recommendations
        )
        assert_err_msg = "_get_recommendations_from_word returned" \
            "wrong number of recommendations"
        assert len(result) == num_recommendations, assert_err_msg

    def test_num_recom_from_get_recommendations_from_vec(self):
        """
        Ensure valid num of recommendations from get_recommendations_from_vec.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 09
        |
        | *Description* : Verify number of recommendations conform to the
        |                number of recommendations requested.
        |                Test
        |                :func:`VectorSpaceMapper.get_recommendations_from_vec`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : num_recommendations
        |
        | *Test Data* : num_recommendations = random.randint(1,10)
        |
        | *Expected Result* : The number of recommendations returned is equal
        |                     to the number of recommendations requested.
        |
        | *Actual Result* : The number of recommendations returned is equal
        |                   to the number of recommendations requested.
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_vec(
            obj.model_1.wv['has'], topn=num_recommendations
        )
        assert_err_msg = "_get_recommendations_from_word returned"\
            "wrong number of recommendations"
        assert len(result) == num_recommendations, assert_err_msg

    def test_get_recommendations_from_word(self):
        """
        Ensure valid types from get_recommendations_from_word.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 10
        |
        | *Description* : Verify the response type of the word and distance
        |               returned from the function.
        |               Test
        |               :func:`VectorSpaceMapper.get_recommendations_from_word`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : word passed to get_recommendations_from_word
        |
        | *Test Data* : word = 'has'
        |
        | *Expected Result* : word_type is unicode, and dist_type is float
        |
        | *Actual Result* : word_type is unicode, and dist_type is float
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        result = obj.get_recommendations_from_word('has')
        word_type, dist_type = (str, float)
        assert_err_msg = "_get_recommendations_from_word" \
            "returned wrong type"
        for word, dist in result:
            assert (
                type(word) is word_type and type(dist) is dist_type
            ), assert_err_msg

    def test_get_recommendations_from_vec(self):
        """
        Ensure valid types from get_recommmendations_from_vec.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 11
        |
        | *Description* : Verify the response type of the word and distance
        |                returned from the function.
        |                Test
        |                :func:`VectorSpaceMapper.get_recommendations_from_vec`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : vector passed to get_recommendations_from_vec
        |
        | *Test Data* : vector = obj.model_1['has']
        |
        | *Expected Result* : word_type is unicode, and dist_type is float
        |
        | *Actual Result* : word_type is unicode, and dist_type is float
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        result = obj.get_recommendations_from_vec(obj.model_1.wv['has'])
        word_type, dist_type = (str, float)
        assert_err_msg = "_get_recommendations_from_word"\
            "returned wrong type"
        for word, dist in result:
            assert (
                type(word) is word_type and type(dist) is dist_type
            ), assert_err_msg

    def test_get_recommendations_from_vec_and_word_match(self):
        """
        Ensure valid recommendations obtained.

        | *Test Suite ID* : V
        |
        | *Test Case Number* : 12
        |
        | *Description* : Verify the results from both functions match.
        |          Test following functions:
        |             - :func:`VectorSpaceMapper.get_recommendations_from_vec`
        |             - :func:`VectorSpaceMapper.get_recommendations_from_word`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : word passed to get_recommendations_from_word, and
        |                     vector passed to get_recommendations_from_vec
        |
        | *Test Data* : word = 'has', vector = obj.model_1['has']
        |
        | *Expected Result* : Recommendations match
        |
        | *Actual Result* : Recommendations match
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        result = dict(obj.get_recommendations_from_word('has'))
        expected = dict(obj.get_recommendations_from_vec(obj.model_1.wv['has']))
        assert_err_msg = "_get_recommendations_from_vec do not match"\
            "_get_recommendations_from_word"
        for word, dist in expected.items():
            assert dist == result[word], assert_err_msg
