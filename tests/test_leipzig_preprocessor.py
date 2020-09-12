#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Unit Test Cases for :mod:`tvecs.preprocessor.leipzig_preprocessor`.

.. py:currentmodule:: tvecs.preprocessor.leipzig_preprocessor
"""

import os
import pytest

from tvecs.preprocessor.leipzig_preprocessor import LeipzigPreprocessor


class TestLeipzigPreprocessor:
    """
    Unit Testing for module :mod:`tvecs.preprocessor.leipzig_preprocessor`.

    Test Cases considered for the following functions
        - :func:`LeipzigPreprocessor._clean_word`
        - :func:`LeipzigPreprocessor._tokenize_words`
        - :func:`LeipzigPreprocessor._tokenize_sentences`

    .. seealso::
        * :mod:`tvecs.preprocessor.base_preprocessor`
        * :mod:`pytest`
    """

    def setup_class(cls):
        """
        Setup Unit Testing for :class:`LeipzigPreprocessor`.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 01
        |
        | *Description* : Create an instance of class LeipzigPreprocessor.
        |                 Tests :class:`LeipzigPreprocessor`
        |
        | *Preconditions* : BaseProcessor exists
        |
        | *Test Parameters* : corpus_fname, corpus_dir_path
        |
        | *Test Data* :
        |    corpus_fname='test_leipzig_corpus',
        |    corpus_dir_path='tests/resources'
        |
        | *Expected Result* : Instance of :class:`LeipzigPreprocessor` created
        |
        | *Actual Result* : Instance of :class:`LeipzigPreprocessor` created
        |
        | **Status : Pass**
        |

        API Documentation:
            :param cls: Class level scope
            :type cls: :class:`TestLeipzigPreprocessor`
        """
        try:
            cls.testing_obj = LeipzigPreprocessor(
                corpus_fname='test_leipzig_corpus',
                corpus_dir_path=os.path.join('tests', 'resources')
            )
        except BaseException as err:
            pytest.fail(
                'Pre-processing %s failed : %s' % (
                    'test_leipzig_corpus', err
                )
            )

    def teardown_class(cls):
        """
        Delete temp files generated for tests.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 02
        |
        | *Description* : Delete the generated preprocessed file
        |                test_leipzig_corpus_processed to remove residual file.
        |
        | *Preconditions* : Preprocessed test_leipzig_corpus_processed
        |                   file exists in the specified path.
        |
        | *Test Parameters* : Preprocessed file path.
        |
        | *Test Data* : path='tests/resources/test_leipzig_corpus_processed'
        |
        | *Expected Result* : Preprocessed file
        |                     test_leipzig_corpus_processed is deleted.
        |
        | *Actual Result* : Preprocessed file
        |                   test_leipzig_corpus_processed is deleted.
        |
        | **Status : Pass**
        |


        API Documentation:
            :param cls: Class level scope
            :type cls: :class:`TestLeipzigPreprocessor`
        """
        try:
            os.remove(
                os.path.join(
                    'tests',
                    'resources',
                    'test_leipzig_corpus.%s' % 'preprocessed'
                )
            )
        except (OSError, IOError):
            pass

    def test_implement_clean_word(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 03
        |
        | *Description* : Ensure that the word level clean functionality
        |                 is implemented in the class.
        |                 Tests :func:`LeipzigPreprocessor._clean_word`
        |
        | *Preconditions* : LeipzigPreprocessor class instance exists.
        |
        | *Test Parameters* : word passed to function.
        |
        | *Test Data* : word=''
        |
        | *Expected Result* : NotImplementedError exception is not raised.
        |
        | *Actual Result* : NotImplementedError exception is not raised.
        |
        | **Status : Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        try:
            testing_object._clean_word(word='')
        except NotImplementedError:
            pytest.fail('Not Implemented _clean_word function')

    def test_implement_tokenize_words(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 04
        |
        | *Description* : Ensure that the word level clean functionality
        |                 is implemented in the class.
        |                 Tests :func:`LeipzigPreprocessor._tokenize_words`
        |
        | *Preconditions* : LeipzigPreprocessor class instance exists.
        |
        | *Test Parameters* : sentence passed to function.
        |
        | *Test Data* : sentence=''
        |
        | *Expected Result* : NotImplementedError exception is not raised.
        |
        | *Actual Result* : NotImplementedError exception is not raised.
        |
        | **Status : Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        try:
            testing_object._tokenize_words(sentence='')
        except NotImplementedError:
            pytest.fail('Not Implemented _tokenize_words function')

    def test_tokenize_words(self):
        """
        Test tokenize word functionality.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 05
        |
        | *Description* : Ensure that the word level clean functionality
        |                 for Hindi words.
        |                 Tests :func:`LeipzigPreprocessor._tokenize_words`
        |
        | *Preconditions* : LeipzigPreprocessor class instance must exist
        |
        | *Test Parameters* : data, which is in Hindi
        |
        | *Test Data* : data = u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से' \
                               u' ला-लाकर घड़े में डालने लगा बस क्या था !'
        |
        | *Expected Result* : [
        |     u"मैं", u"आसपास", u"बिखरे", u"पड़े", u"कंकड़-पत्थर",
        |     u"चोंच", u"से", u"ला-लाकर",
        |     u"घड़े", u"में", u"डालने", u"लगा", u"बस", u"क्या", u"था", u"!"
        | ]
        |
        | *Actual Result* : [
        |    u"मैं", u"आसपास", u"बिखरे", u"पड़े", u"कंकड़-पत्थर",
        |    u"चोंच", u"से", u"ला-लाकर",
        |    u"घड़े", u"में", u"डालने", u"लगा", u"बस", u"क्या", u"था", u"!"
        | ]
        |
        | **Status : Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        data = u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से' \
               u' ला-लाकर घड़े में डालने लगा बस क्या था !'
        expected = [
            u"मैं", u"आसपास", u"बिखरे", u"पड़े", u"कंकड़-पत्थर", u"चोंच",
            u"से", u"ला-लाकर", u"घड़े", u"में", u"डालने",
            u"लगा", u"बस", u"क्या", u"था", u"!"
        ]
        result = testing_object._tokenize_words(data)
        assert result == expected, "_tokenize_words failed"

    def test_hindi_clean_word(self):
        """
        Test clean word functionality for hindi.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 06
        |
        | *Description* : Ensure that the word level clean functionality
        |                  works for Hindi.
        |                 -bringing to lower case
        |                 -removing punctuation, special characters and digits
        |                 Tests :func:`LeipzigPreprocessor._clean_word`
        |
        | *Preconditions* : LeipzigPreprocessor class instance exists
        |
        | *Test Parameters* : data, which is in Hindi
        |
        | *Test Data* : data = [
        |    u'मैं', u'आसपास', u'बिखरे', u'पड़े', u'कंकड़-पत्थर,',
        |    u'चोंच', u'से', u'ला-लाकर', u'घड़े', u'में!',
        |    u'Bleh', u'डालने', u'लगा', u'बस.', u'क्या', u'था', u'!'
        | ]
        |
        | *Expected Result* : [
        |    [u'मैं'], [u'आसपास'], [u'बिखरे'], [u'पड़े'], [u'कंकड़', u'पत्थर'],
        |    [u'चोंच'], [u'से'], [u'ला', u'लाकर'], [u'घड़े'],
        |    [u'में'], [], [u'डालने'], [u'लगा'], [u'बस'],
        |    [u'क्या'], [u'था'], []
        | ]
        |
        | *Actual Result* : [
        |     [u'मैं'], [u'आसपास'], [u'बिखरे'], [u'पड़े'],
        |     [u'कंकड़', u'पत्थर'], [u'चोंच'], [u'से'],
        |     [u'ला', u'लाकर'], [u'घड़े'], [u'में'], [], [u'डालने'], [u'लगा'],
        |     [u'बस'], [u'क्या'], [u'था'], []
        | ]
        |
        | **Status: Pass**
        |


        """
        testing_object = self.__class__.testing_obj
        data = [
            u'मैं', u'आसपास', u'बिखरे', u'पड़े', u'कंकड़-पत्थर,', u'चोंच', u'से',
            u'ला-लाकर', u'घड़े', u'में!', u'Bleh', u'डालने', u'लगा',
            u'बस.', u'क्या', u'था', u'!'
        ]
        expected = [
            [u'मैं'], [u'आसपास'], [u'बिखरे'], [u'पड़े'], [u'कंकड़', u'पत्थर'],
            [u'चोंच'], [u'से'], [u'ला', u'लाकर'], [u'घड़े'], [u'में'],
            [], [u'डालने'], [u'लगा'], [u'बस'], [u'क्या'], [u'था'], []
        ]
        testing_object.language = 'hindi'
        assert_err_msg = "_clean_word function failed for Hindi"
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], assert_err_msg
        testing_object.language = 'english'

    def test_english_clean_word(self):
        """
        Test clean word functionality for english.

        | *Test Suite ID* : L
        |
        | *Test Case Number* : 07
        |
        | *Description* : Ensure that the word level clean functionality
        |                 works for English.
        |                 -bringing to lower case
        |                 -removing punctuation, special characters and digits
        |                 -special handling of apostrophes and hyphen
        |                 Tests :func:`LeipzigPreprocessor._clean_word`
        |
        | *Preconditions* : LeipzigPreprocessor class instance exists
        |
        | *Test Parameters* : data, which is in English
        |
        | *Test Data* : data = [
        |    'Typed', 'essays', 'are', 'preferred', 'but',
        |    'this', 'is', 'not', 'essential.', "you'll",
        |    "tables'", 'ice-cream', u"they’re"
        | ]
        | *Expected Result* : [
        |    ['typed'], ['essays'], ['are'], ['preferred'],
        |    ['but'], ['this'], ['is'], ['not'], ['essential'],
        |    ['you'], ['tables'], ['ice', 'cream'], [u"they"]
        | ]
        |
        | *Actual Result*: [
        |     ['typed'], ['essays'], ['are'], ['preferred'],
        |     ['but'], ['this'], ['is'], ['not'], ['essential'],
        |     ['you'], ['tables'], ['ice', 'cream'], [u"they"]
        | ]
        |
        | **Status: Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        data = [
            'Typed', 'essays', 'are', 'preferred', 'but',
            'this', 'is', 'not', 'essential.', "you'll",
            "tables'", 'ice-cream', u"they’re"
        ]
        expected = [
            ['typed'], ['essays'], ['are'], ['preferred'],
            ['but'], ['this'], ['is'], ['not'], ['essential'],
            ['you'], ['tables'], ['ice', 'cream'], [u"they"]
        ]
        assert_err_msg = "_clean_word function failed for English"
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], assert_err_msg
