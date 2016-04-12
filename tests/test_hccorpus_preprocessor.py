#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import pytest
from modules.preprocessor.hccorpus_preprocessor import HcCorpusPreprocessor

class TestHcCorpusPreprocessor:

    def setup_class(cls):
        try:
            cls.testing_obj = HcCorpusPreprocessor(
                corpus_fname='test_hccorpus_corpus',
                corpus_dir_path=os.path.join('tests', 'resources'),
                need_preprocessing=True
            )
        except BaseException as err:
            pytest.fail(
                'Pre-processing %s failed : %s' %('test_hccorpus_corpus', err.message)
            )

    def teardown_class(cls):
        try:
            os.remove(
                os.path.join('tests', 'resources', 'test_hccorpus_corpus.%s' % 'preprocessed')
            )
        except (OSError, IOError) as err:
            pass

    def test_implement_extract_corpus_data(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._extract_corpus_data(data='')
        except NotImplementedError:
            pytest.fail('Not Implemented _extract_corpus_data function')

    def test_implement_clean_word(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._clean_word(word='')
        except NotImplementedError:
            pytest.fail('Not Implemented _clean_word function')

    def test_implement_tokenize_sentences(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._tokenize_sentences(data='')
        except NotImplementedError:
            pytest.fail('Not Implemented _tokenize_sentences function')

    def test_implement_tokenize_words(self):
        testing_object = self.__class__.testing_obj
        try:
            testing_object._tokenize_words(sentence='')
        except NotImplementedError:
            pytest.fail('Not Implemented _tokenize_words function')

    def test_extract_corpus_data(self):
        """Bleh is the problem"""
        testing_object = self.__class__.testing_obj
        data = """blogspot.com\t2011/10/01\t3\t0\tWe love you Mr. Brown.
            blogspot.com\t2012/01/01\t3\t0\tIf I were a bear,"""
        expected = 'We love you Mr. Brown.. If I were a bear,'
        result = testing_object._extract_corpus_data(data=data)
        assert result == expected, "_extract_corpus_data implementation failed"

    def test_english_tokenize_sentences(self):
        testing_object = self.__class__.testing_obj
        data = 'We love you Mr. Brown.. If I were a bear,'
        expected = ['We love you Mr. Brown..', 'If I were a bear,']
        result = list(testing_object._tokenize_sentences(data))
        assert expected == result, "_tokenize_sentences failed for english language"

    def test_hindi_tokenize_sentences(self):
        testing_object = self.__class__.testing_obj
        data = u"ये कहानी तो मेरे को मेरे नाना ने सुनाई थी. गरमी का मौसम था ….." \
               u" सभी नदियाँ, तालाब , कुँए सूख गये थे. पानी का नामोनिशान तक ना था." \
               u" तेज धूप से मुझे बहुत प्यास लग गयी थी , पानी की तलाश में इधर-उधर उड़ता रहा ."\
               u" थक-हार कर एक पेड़ पर जा बैठा तो मुझे एक घड़ा दिखाई दिया ."\
               u" घड़े में पानी बहुत नीचे था और मेरी चोंच पानी तक नहीं पहुँच पा रही थी ."\
               u" मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर घड़े में डालने लगा बस क्या था !"\
               u" पानी धीरे-धीरे घड़े के मुँह तक आ गया । मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया ."
        expected = [
            u'ये कहानी तो मेरे को मेरे नाना ने सुनाई थी.',
            u'गरमी का मौसम था ….. सभी नदियाँ, तालाब , कुँए सूख गये थे.',
            u'पानी का नामोनिशान तक ना था.',
            u'तेज धूप से मुझे बहुत प्यास लग गयी थी , पानी की तलाश में इधर-उधर उड़ता रहा .',
            u'थक-हार कर एक पेड़ पर जा बैठा तो मुझे एक घड़ा दिखाई दिया .',
            u'घड़े में पानी बहुत नीचे था और मेरी चोंच पानी तक नहीं पहुँच पा रही थी .',
            u'मैं आसपास बिखरे पड़े कंकड़-पत्थर चोंच से ला-लाकर घड़े में डालने लगा बस क्या था !',
            u'पानी धीरे-धीरे घड़े के मुँह तक आ गया',
            u'मैंने पानी पीकर अपनी प्यास बुझायी और उड़ गया .'
        ]
        testing_object.language = 'hindi'
        result = list(testing_object._tokenize_sentences(data))
        testing_object.language = 'english'
        max_len = len(result) if len(result) >= len(expected) else len(expected)
        try:
            for i in range(max_len):
                assert expected[i] == result[i], "_tokenize_sentences failed for hindi language: Line => %s" % str(i)
        except IndexError as err:
            pytest.fail("_tokenize_sentences failed for hindi language : %s" % err.message)

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
            'this', 'is', 'not', 'essential.'
        ]
        expected = [
            ['typed'], ['essays'], ['are'], ['preferred'],
            ['but'], ['this'], ['is'], ['not'], ['essential']
        ]
        for i in range(len(data)):
            result = testing_object._clean_word(data[i])
            assert result == expected[i], "_clean_word function failed for Hindi"
