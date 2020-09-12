#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Unit Test Cases for :mod:`tvecs.preprocessor.emille_preprocessor`.

.. py:currentmodule:: tvecs.preprocessor.emille_preprocessor
"""

import os
import pytest

from tvecs.preprocessor.emille_preprocessor import EmilleCorpusPreprocessor


class TestEmilleCorpusPreprocessor:
    """
    Unit Testing for module :mod:`tvecs.preprocessor.emille_preprocessor`.

    Test Cases considered for the following functions
        - :func:`EmilleCorpusPreprocessor._extract_corpus_data`
        - :func:`EmilleCorpusPreprocessor._clean_word`
        - :func:`EmilleCorpusPreprocessor._tokenize_sentences`
        - :func:`EmilleCorpusPreprocessor._tokenize_words`

    .. seealso::
        * :mod:`tvecs.preprocessor.base_preprocessor`
        * :mod:`pytest`
    """

    def setup_class(cls):
        """
        Setup Unit Testing for :class:`EmilleCorpusPreprocessor`.

        | *Test Suite ID* : E.
        |
        | *Test Case Number* : 01
        |
        | *Description* : Create an instance of class EmilleCorpusPreprocessor
        |                 Tests :class:`EmilleCorpusPreprocessor`
        |
        | *Preconditions* : BaseProcessor exists
        |
        | *Test Parameters* : corpus_fname, corpus_dir_path, need_preprocessing
        |
        | *Test Data* :
        |    corpus_fname='test_emille_corpus',
        |    corpus_dir_path='tests/resources',
        |    need_preprocessing=True
        |
        | *Expected Result* : Instance of
        |                     :class:`EmilleCorpusPreprocessor` created
        |
        | *Actual Result* : Instance of
        |                   :class:`EmilleCorpusPreprocessor` created
        |
        | **Status : Pass**
        |

        API Documentation:
            :param cls: Class level scope
            :type cls: :class:`TestEmilleCorpusPreprocessor`
        """
        try:
            cls.testing_obj = EmilleCorpusPreprocessor(
                corpus_fname='test_emille_corpus',
                corpus_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True
            )
        except BaseException as err:
            pytest.fail(
                'Pre-processing %s failed : %s' % (
                    'test_emille_corpus', err
                )
            )

    def teardown_class(cls):
        """
        Delete temp files generated for tests.

        | *Test Suite ID* : E.
        |
        | *Test Case Number* : 02
        |
        | *Description* : Delete the generated preprocessed file
        |                 test_emille_corpus_processed to remove residual file.
        |
        | *Preconditions* : Preprocessed test_emille_corpus_processed
        |                   file exists in the specified path
        |
        | *Test Parameters* : Preprocessed file path
        |
        | *Test Data* : path='tests/resources/test_emille_corpus_processed'
        |
        | *Expected Result* : Preprocessed file
        |                     test_emille_corpus_processed is deleted
        |
        | *Actual Result* : Preprocessed file
        |                   test_emille_corpus_processed is deleted
        |
        | **Status : Pass**
        |

        API Documentation:
            :param cls: Class level scope
            :type cls: :class:`TestEmilleCorpusPreprocessor`
        """
        try:
            os.remove(
                os.path.join(
                    'tests',
                    'resources',
                    'test_emille_corpus.%s' % 'preprocessed'
                )
            )
        except (OSError, IOError):
            pass
        pass

    def test_implement_extract_corpus_data(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 03
        |
        | *Description* : Ensure the corpus data extract functionality
        |                 is implemented in the class.
        |                 Test
        |                 :func:`EmilleCorpusPreprocessor._extract_corpus_data`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance exists
        |
        | *Test Parameters* : data passed to function
        |
        | *Test Data* : data=''
        |
        | *Expected Result* : NotImplementedError exception is not raised
        |
        | *Actual Result* : NotImplementedError exception is not raised
        |
        | **Status : Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        try:
            testing_object._extract_corpus_data(data='')
        except NotImplementedError:
            pytest.fail('Not Implemented _extract_corpus_data function')

    def test_implement_clean_word(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 04
        |
        | *Description* : Ensure that the word level clean functionality
        |                 is implemented in the class
        |                 Test :func:`EmilleCorpusPreprocessor._clean_word`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance exists
        |
        | *Test Parameters* : word passed to function
        |
        | *Test Data* : word=''
        |
        | *Expected Result* : NotImplementedError exception is not raised
        |
        | *Actual Result* : NotImplementedError exception is not raised
        |
        | **Status : Pass**

        """
        testing_object = self.__class__.testing_obj
        try:
            testing_object._clean_word(word='')
        except NotImplementedError:
            pytest.fail('Not Implemented _clean_word function')

    def test_implement_tokenize_sentences(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 05
        |
        | *Description* : Ensure that the sentence tokenize functionality
        |                 is implemented in the class.
        |                 Test
        |                 :func:`EmilleCorpusPreprocessor._tokenize_sentences`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance exists
        |
        | *Test Parameters* : data passed to function
        |
        | *Test Data* : data=''
        |
        | *Expected Result* : NotImplementedError exception is not raised
        |
        | *Actual Result* : NotImplementedError exception is not raised
        |
        | **Status : Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        try:
            testing_object._tokenize_sentences(data='')
        except NotImplementedError:
            pytest.fail('Not Implemented _tokenize_sentences function')

    def test_implement_tokenize_words(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 06
        |
        | *Description* : Ensure that the word tokenize functionality
        |                 is implemented in the class.
        |                 Test :func:`EmilleCorpusPreprocessor._tokenize_words`
        |
        | *Preconditions* : :class:`EmilleCorpusPreprocessor` instance exists.
        |
        | *Test Parameters* : sentence passed to function
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

    def test_extract_corpus_data(self):
        """
        Ensure functionality is implemented.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 07
        |
        | *Description* : Ensure preprocessor can extract required corpus
        |                 and remove unnecessary data.
        |                 Test
        |                 :func:`EmilleCorpusPreprocessor._extract_corpus_data`
        |
        | *Preconditions* : :class:`EmilleCorpusPreprocessor` instance exists
        |
        | *Test Parameters* : data passed to function.
        |
        | *Test Data* : data = "<p>अवध-स्कूल के चित्रों का सर्वाधिक विशिष्ट</p>
        |               random text which needs to be removed during extraction
        |               <p>बनाये गये हैं। चित्रों में पीले रंग का</p>
        |               more random text"
        |
        | *Expected Result* : "अवध-स्कूल के चित्रों का सर्वाधिक " \
        |                     "विशिष्ट. बनाये गये हैं। चित्रों में पीले रंग का"
        |
        | *Actual Result* : "अवध-स्कूल के चित्रों का सर्वाधिक " \
        |                   "विशिष्ट. बनाये गये हैं। चित्रों में पीले रंग का"
        |
        | **Status : Pass**
        |
        """
        testing_object = self.__class__.testing_obj
        data = u"<p>अवध-स्कूल के चित्रों का सर्वाधिक विशिष्ट</p>" \
            u"random text which needs to be removed during extraction" \
            u"<p>बनाये गये हैं। चित्रों में पीले रंग का</p>" \
            u"more random text"
        expected = u"अवध-स्कूल के चित्रों का सर्वाधिक विशिष्ट. बनाये गये" \
            u" हैं। चित्रों में पीले रंग का"
        result = testing_object._extract_corpus_data(data=data)
        assert result == expected, "_extract_corpus_data implementation failed"

    def test_english_tokenize_sentences(self):
        """
        Ensure sentence tokenize works as expected.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 08
        |
        | *Description* : Ensure that the sentence tokenize functionality
        |                 for English works as expected.
        |                 Test
        |                 :func:`EmilleCorpusPreprocessor._tokenize_sentences`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance exists
        |
        | *Test Parameters* : data, which is in English
        |
        | *Test Data* : data = 'We love you Mr. Brown.. If I were a bear,'
        |
        | *Expected Result* : ['We love you Mr. Brown..', 'If I were a bear,']
        |
        | *Actual Result* : ['We love you Mr. Brown..', 'If I were a bear,']
        |
        | **Status: Pass**
        |


        """
        testing_object = self.__class__.testing_obj
        data = 'We love you Mr. Brown.. If I were a bear,'
        expected = ['We love you Mr. Brown..', 'If I were a bear,']
        result = list(testing_object._tokenize_sentences(data))
        assert_err_msg = "_tokenize_sentences failed for english language"
        assert expected == result, assert_err_msg

    def test_hindi_tokenize_sentences(self):
        """
        Ensure tokenize sentences works for hindi corpus.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 09
        |
        | *Description* : Ensure that the sentence tokenize functionality
        |                 works for Hindi as expected as expected.
        |                 Test
        |                 :func:`EmilleCorpusPreprocessor._tokenize_sentences`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance exists
        |
        | *Test Parameters* : data, which is in Hindi
        |
        | *Test Data* : data = u"ये कहानी तो मेरे को मेरे" \
        |       u" नाना ने सुनाई थी. गरमी का मौसम था ….." \
        |       u" सभी नदियाँ, तालाब , कुँए सूख गये थे." \
        |       u" पानी का नामोनिशान तक ना था." \
        |       u" तेज धूप से मुझे बहुत प्यास लग गयी थी ," \
        |       u" पानी की तलाश में इधर-उधर उड़ता रहा ." \
        |       u" थक-हार कर एक पेड़ पर जा बैठा तो मुझे" \
        |       u" एक घड़ा दिखाई दिया ." \
        |       u" घड़े में पानी बहुत नीचे था और मेरी चोंच" \
        |       u" पानी तक नहीं पहुँच पा रही थी ." \
        |       u" मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से" \
        |       u" ला-लाकर घड़े में डालने लगा बस क्या था !" \
        |       u" पानी धीरे-धीरे घड़े के मुँह तक आ गया । मैंने" \
        |       u" पानी पीकर अपनी प्यास बुझायी और उड़ गया ."
        |
        | *Expected Result* : [
        |    u'ये कहानी तो मेरे को मेरे नाना ने सुनाई थी.',
        |    u'गरमी का मौसम था ….. सभी नदियाँ, तालाब , कुँए सूख गये थे.',
        |    u'पानी का नामोनिशान तक ना था.',
        |    u'तेज धूप से मुझे बहुत प्यास लग गयी थी ,' \
        |    u' पानी की तलाश में इधर-उधर उड़ता रहा .',
        |    u'थक-हार कर एक पेड़ पर जा बैठा तो मुझे एक घड़ा दिखाई दिया .',
        |    u'घड़े में पानी बहुत नीचे था और मेरी चोंच पानी' \
        |    u' तक नहीं पहुँच पा रही थी .',
        |    u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर' \
        |    u' घड़े में डालने लगा बस क्या था !',
        |    u'पानी धीरे-धीरे घड़े के मुँह तक आ गया',
        |    u'मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया .'
        |
        | *Actual Result* : [
        |    u'ये कहानी तो मेरे को मेरे नाना ने सुनाई थी.',
        |    u'गरमी का मौसम था ….. सभी नदियाँ, तालाब , कुँए सूख गये थे.',
        |    u'पानी का नामोनिशान तक ना था.',
        |    u'तेज धूप से मुझे बहुत प्यास लग गयी थी ,' \
        |    u' पानी की तलाश में इधर-उधर उड़ता रहा .',
        |    u'थक-हार कर एक पेड़ पर जा बैठा तो मुझे एक घड़ा दिखाई दिया .',
        |    u'घड़े में पानी बहुत नीचे था और मेरी चोंच' \
        |    u' पानी तक नहीं पहुँच पा रही थी .',
        |    u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर घड़े' \
        |    u' में डालने लगा बस क्या था !',
        |    u'पानी धीरे-धीरे घड़े के मुँह तक आ गया',
        |    u'मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया .'
        |
        | **Status: Pass**
        |

        """
        testing_object = self.__class__.testing_obj
        data = u"ये कहानी तो मेरे को मेरे नाना ने सुनाई" \
               u" थी. गरमी का मौसम था ….." \
               u" सभी नदियाँ, तालाब , कुँए सूख गये थे." \
               u" पानी का नामोनिशान तक ना था." \
               u" तेज धूप से मुझे बहुत प्यास लग गयी थी ," \
               u" पानी की तलाश में इधर-उधर उड़ता रहा ." \
               u" थक-हार कर एक पेड़ पर जा बैठा तो मुझे" \
               u" एक घड़ा दिखाई दिया ." \
               u" घड़े में पानी बहुत नीचे था और मेरी चोंच" \
               u" पानी तक नहीं पहुँच पा रही थी ." \
               u" मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से" \
               u" ला-लाकर घड़े में डालने लगा बस क्या था !" \
               u" पानी धीरे-धीरे घड़े के मुँह तक आ गया ।" \
               u" मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया ."
        expected = [
            u'ये कहानी तो मेरे को मेरे नाना ने सुनाई थी.',
            u'गरमी का मौसम था ….. सभी नदियाँ, तालाब , कुँए सूख गये थे.',
            u'पानी का नामोनिशान तक ना था.',
            u'तेज धूप से मुझे बहुत प्यास लग गयी थी , पानी'
            u' की तलाश में इधर-उधर उड़ता रहा .',
            u'थक-हार कर एक पेड़ पर जा बैठा तो मुझे एक घड़ा दिखाई दिया .',
            u'घड़े में पानी बहुत नीचे था और मेरी चोंच पानी तक नहीं'
            u' पहुँच पा रही थी .',
            u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर'
            u' घड़े में डालने लगा बस क्या था !',
            u'पानी धीरे-धीरे घड़े के मुँह तक आ गया',
            u'मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया .'
        ]
        testing_object.language = 'hindi'
        result = list(testing_object._tokenize_sentences(data))
        testing_object.language = 'english'
        max_len = len(result) if len(result) >= len(expected) else len(
            expected
        )
        assert_err_msg = (
            "_tokenize_sentences failed for hindi language: %s"
        )
        try:
            for i in range(max_len):
                assert expected[i] == result[i], assert_err_msg % (
                    'Line => ' + str(i)
                )
        except IndexError as err:
            pytest.fail(assert_err_msg % err)

    def test_tokenize_words(self):
        """
        Test tokenize word functionality.

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 10
        |
        | *Description* : Ensure that the word tokenize functionality
        |                 works as expected.
        |                 Test :func:`EmilleCorpusPreprocessor._tokenize_words`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance must exist
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

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 11
        |
        | *Description* : Ensure that the word level clean functionality
        |                 works for Hindi as expected.
        |                 Tests :func:`EmilleCorpusPreprocessor._clean_word`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance must exist
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

        | *Test Suite ID* : E
        |
        | *Test Case Number* : 12
        |
        | *Description* : Ensure that the word level clean functionality
        |                 works for English as expected
        |                 Tests :func:`EmilleCorpusPreprocessor._clean_word`
        |
        | *Preconditions* : EmilleCorpusPreprocessor class instance must exist
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
        assert_err_msg = "_clean_word function failed for Hindi"
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], assert_err_msg
