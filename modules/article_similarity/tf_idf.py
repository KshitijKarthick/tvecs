#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to Perform tf-idf utilised for document similarity."""

import os
import glob
import codecs
import itertools
import numpy as np
import scipy
from sklearn.cluster import AffinityPropagation
from gensim.models import Word2Vec
from modules.vector_space_mapper.vector_space_mapper import VectorSpaceMapper
from sklearn.feature_extraction.text import TfidfVectorizer


def get_cmp_func(model_1, model_2, bilingual_dict, cross_lingual=True):
    """Return the comparison function based on cross_lingual or not."""
    func = None
    if cross_lingual is True:
        vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
        vm.map_vector_spaces()
        func = vm._predict_vec_from_word
    else:
        def get_vec(word):
            model_1[word]
        func = get_vec
    return func


def _load_models(cross_lingual=True):
    if cross_lingual is True:
        model_1 = Word2Vec.load(
            os.path.join('data', 'models', 't-vex-english-model')
        )
        model_2 = Word2Vec.load(
            os.path.join('data', 'models', 't-vex-hindi-model')
        )
        with codecs.open(
            os.path.join(
                'data', 'bilingual_dictionary', 'english_hindi_train_bd'
            ), 'r', encoding='utf-8'
        ) as file:
            data = file.read().split('\n')
            bilingual_dict = [
                (line.split(' ')[0], line.split(' ')[1])
                for line in data
            ]
            vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
            vm.map_vector_spaces()
            kwargs = {
                'model_1': model_1,
                'model_2': model_2,
                'bilingual_dict': bilingual_dict,
                'cross_lingual': True
            }
    else:
        model_1 = Word2Vec.load(
            os.path.join('data', 'models', 't-vex-english-model')
        )
        kwargs = {
            'model_1': model_1,
            'model_2': model_1,
            'bilingual_dict': [],
            'cross_lingual': False
        }
    return kwargs


def top_words(scores, words, n=10):
    """Return top n words using tf-idf."""
    l = {word: score for word, score in zip(words, scores)}
    return sorted(l, key=l.__getitem__)[:n]


if __name__ == '__main__':
    kwargs = _load_models(cross_lingual=True)
    tr = get_cmp_func(**kwargs)
    tf1 = TfidfVectorizer(input="file", min_df=1, stop_words='english')
    english_articles = glob.glob(
        os.path.join("data", "blogs", "English") + os.path.sep + "*"
    )
    english_articles_obj = [
        codecs.open(f, 'r', encoding='utf-8') for f in english_articles
    ]
    hindi_articles = glob.glob(
        os.path.join("data", "blogs", "Hindi") + os.path.sep + "*"
    )
    tfidf_matrix1 = tf1.fit_transform(english_articles_obj)
    dense_mat1 = tfidf_matrix1.todense().tolist()
    for f in english_articles_obj:
        f.close()
    tf2 = TfidfVectorizer(input="file", min_df=1, stop_words='english')
    hindi_articles_obj = [
        codecs.open(f, 'r', encoding='utf-8') for f in hindi_articles
    ]
    tfidf_matrix2 = tf2.fit_transform(hindi_articles_obj)
    dense_mat2 = tfidf_matrix2.todense().tolist()
    for f in english_articles_obj:
        f.close()
    z = {}
    for ((l1, l2), (index1, index2)) in zip(
            itertools.product(
                dense_mat1, dense_mat2
            ), itertools.product(
                range(1, 21), range(1, 21)
            )
    ):
        words1 = top_words(l1, tf1.get_feature_names())
        words2 = top_words(l2, tf2.get_feature_names())

        word_vectors1 = []
        word_vectors2 = []

        for word in words1:
            try:
                word_vectors1.append(tr(word))
            except:
                pass

        for word in words2:
            try:
                word_vectors2.append(kwargs['model_2'][word])
            except:
                pass
        distance = scipy.spatial.distance.euclidean(
            np.mean(word_vectors1, axis=0),
            np.mean(word_vectors2, axis=0)
        )
        z[
            (english_articles[index1 - 1], hindi_articles[index2 - 1])
        ] = distance

    l = sorted(z.items(), key=lambda (x, y): y, reverse=True)
    for x in l:
        print x
