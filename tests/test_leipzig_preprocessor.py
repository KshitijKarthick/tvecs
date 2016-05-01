#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import pytest

from tvecs.preprocessor.leipzig_preprocessor import LeipzigPreprocessor

class TestHcCorpusPreprocessor:

    def setup_class(cls):
        try:
            cls.testing_obj = LeipzigPreprocessor(
                corpus_fname='test_leipzig_corpus',
                corpus_dir_path=os.path.join('tests', 'resources')
            )
        except BaseException as err:
            pytest.fail(
                'Pre-processing %s failed : %s' %('test_leipzig_corpus', err.message)
            )

    def teardown_class(cls):
        try:
            os.remove(
                os.path.join('tests', 'resources', 'test_leipzig_corpus.%s' % 'preprocessed')
            )
        except (OSError, IOError) as err:
            pass

    def test_implement_clean_word(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._clean_word(word='')
        except NotImplementedError:
            pytest.fail('Not Implemented _clean_word function')

    def test_implement_tokenize_words(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._tokenize_words(sentence='')
        except NotImplementedError:
            pytest.fail('Not Implemented _tokenize_words function')

    def test_tokenize_words(self):
        testing_object = self.__class__.testing_obj
        data = u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर घड़े में डालने लगा बस क्या था !'
        expected = [
            u"मैं", u"आसपास", u"बिखरे", u"पड़े", u"कंकड़-पत्थर", u"चोंच", u"से", u"ला-लाकर",
            u"घड़े", u"में", u"डालने", u"लगा", u"बस", u"क्या", u"था", u"!"
        ]
        result = testing_object._tokenize_words(data)
        assert result == expected, "_tokenize_words failed"

    def test_hindi_clean_word(self):
        testing_object = self.__class__.testing_obj
        data = [
            u'मैं', u'आसपास', u'बिखरे', u'पड़े', u'कंकड़-पत्थर,', u'चोंच', u'से',
            u'ला-लाकर', u'घड़े', u'में!', u'Bleh', u'डालने', u'लगा', u'बस.', u'क्या', u'था', u'!'
        ]
        expected = [
            [u'मैं'], [u'आसपास'], [u'बिखरे'], [u'पड़े'], [u'कंकड़', u'पत्थर'], [u'चोंच'], [u'से'],
            [u'ला', u'लाकर'], [u'घड़े'], [u'में'], [],[u'डालने'], [u'लगा'], [u'बस'], [u'क्या'], [u'था'], []
        ]
        testing_object.language = 'hindi'
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], "_clean_word function failed for Hindi"
        testing_object.language = 'english'

    def test_english_clean_word(self):
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
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], "_clean_word function failed for Hindi"
