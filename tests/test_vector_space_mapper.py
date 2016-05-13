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
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 01
        |
        | *Description* : Create an instance of :mod:`tvecs.vector_space_mapper.vector_space_mapper`
        |
        | *Preconditions* : Corpus data for both languages, and bilingual dictionary exists
        |
        | *Test Parameters* : model_1, model_2, bilingual_dict
        |
        | *Test Data* : model_1 = English, model_2 = Hindi, bilingual_dict = 'data/bilingual_dictionary/english_hindi_train_bd'
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
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 02
        |
        | *Description* : Delete models after construction to remove residual of setup_test [Test Case Number 01]
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
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 03
        |
        | *Description* : Verify the data structure for the response of the function for English model.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._extract_vectors_and_words`
        |
        | *Preconditions* : The English model exists
        |
        | *Test Parameters* : model_1 and expected_list[keys]
        |
        | *Test Data* : model_1 is English model, expected_list[keys] = {u'has', u'have', u'\u0915\u093e'}
        |
        | *Expected Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
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

        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, "_extract_vectors_and_words failed for english model [ Data Structure test ]"

    def test_hindi_extract_vectors_and_words(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 04
        |
        | *Description* : Verify the data structure for the response of the function for Hindi model.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._extract_vectors_and_words`
        |
        | *Preconditions* : The Hindi model exists
        |
        |
        | *Test Parameters* : model_2 and expected_list[keys]
        |
        | *Test Data* : model_2 is Hindi model, expected_list[keys] = {u'\u0915\u093e', u'\u0925\u0940', u'english'}
        |
        | *Expected Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
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

        result = dict(zip(result_word, temp_list))
        for key, value in expected_list.items():
            assert result[key] == value, "_extract_vectors_and_words failed for hindi model [ Data Structure test ]"

    def test_predict_vec_from_word(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 05
        |
        | *Description* : Verify the data structure for the response of the function given a word.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_word`
        |
        | *Preconditions* : English model exists 
        |
        | *Test Parameters* : word passed to _predict_vec_from_word
        |
        | *Test Data* : word = u'has'
        |
        | *Expected Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |


        """
        obj = self.__class__.testing_obj
        expected = (100,)
        result = obj._predict_vec_from_word('has').shape
        assert expected == result, "_predict_vec_from_word execution failed [ Data Structure test ]"

    def test_predict_vec_from_vec(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 06
        |
        | *Description* : Verify the data structure for the response of the function given a vector.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_vec`
        |
        | *Preconditions* : English model exists 
        |
        | *Test Parameters* : vector passed to _predict_vec_from_vec
        |
        | *Test Data* : vector = obj.model_1['has']
        |
        | *Expected Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | *Actual Result* : Data structure consists of 1 vector of 100 dimensions if word exists in model, else None
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        expected_shape = (100,)
        result_shape = obj._predict_vec_from_vec(
            obj.model_1['has']
        ).shape
        assert expected_shape == result_shape, "_predict_vec_from_vec failed [ Data Structure test ]"

    def test_predict_vec_from_word_and_vec_match(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 07
        |
        | *Description* : Verify both functions provide same predictions.
        |                 Test following functions:
        |                    - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_vec`.
        |                    - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper._predict_vec_from_word`.
        |
        | *Preconditions* : English model exists
        |
        | *Test Parameters* : vector passed to _predict_vec_from_vec, word passed to _predict_vec_from_word
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
            obj.model_1['has']
        )
        expected = obj._predict_vec_from_word('has')

        assert all(result == expected), "Recommendations from _predict_vec_from_vec "\
            "and _predict_vec_from_word do not match"

    def test_num_recom_from_get_recommendations_from_word(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 08
        |
        | *Description* : Verify number of recommendations conform to the number of recommendations requested.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : num_recommendations
        |
        | *Test Data* : num_recommendations = random.randint(1,10)
        |
        | *Expected Result* : The number of recommendations returned is equal to the number of recommendations requested
        |
        | *Actual Result* : The number of recommendations returned is equal to the number of recommendations requested
        |
        | **Status : Pass**
        |
        

        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_word('has', topn=num_recommendations)
        assert len(result) == num_recommendations, "_get_recommendations_from_word returned"\
            "wrong number of recommendations"

    def test_num_recom_from_get_recommendations_from_vec(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 09
        |
        | *Description* : Verify number of recommendations conform to the number of recommendations requested.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : num_recommendations
        |
        | *Test Data* : num_recommendations = random.randint(1,10)
        |
        | *Expected Result* : The number of recommendations returned is equal to the number of recommendations requested
        |
        | *Actual Result* : The number of recommendations returned is equal to the number of recommendations requested
        |
        | **Status : Pass**
        |

        """
        obj = self.__class__.testing_obj
        num_recommendations = random.randint(1, 10)
        result = obj.get_recommendations_from_vec(obj.model_1['has'], topn=num_recommendations)
        assert len(result) == num_recommendations, "_get_recommendations_from_word returned"\
            "wrong number of recommendations"

    def test_get_recommendations_from_word(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 10
        |
        | *Description* : Verify the response type of the word and distance returned from the function.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`
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
        word_type, dist_type = (unicode, float)
        for word, dist in result:
            assert type(word) is word_type and type(dist) is dist_type, "_get_recommendations_from_word"\
                "returned wrong type"

    def test_get_recommendations_from_vec(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 11
        |
        | *Description* : Verify the response type of the word and distance returned from the function.
        |                 Test :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec
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
        result = obj.get_recommendations_from_vec(obj.model_1['has'])
        word_type, dist_type = (unicode, float)
        for word, dist in result:
            assert type(word) is word_type and type(dist) is dist_type, "_get_recommendations_from_word"\
                "returned wrong type"

    def test_get_recommendations_from_vec_and_word_match(self):
        """
        | *Test Suite ID* : V
        |
        | *Test Case Number* : 12
        |
        | *Description* : Verify the results from both functions match.
        |                 Test following functions:
        |                   - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_vec`
        |                   - :func:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper.get_recommendations_from_word`
        |
        | *Preconditions* : English and Hindi models exist
        |
        | *Test Parameters* : word passed to get_recommendations_from_word, and vector passed to get_recommendations_from_vec
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
        expected = dict(obj.get_recommendations_from_vec(obj.model_1['has']))
        for word, dist in expected.items():
            assert dist == result[word], "_get_recommendations_from_vec do not match"\
                "_get_recommendations_from_word"
