#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to Perform tf-idf utilised for document similarity."""

import os
import codecs
import itertools
from gensim.models import Word2Vec
from modules.vector_space_mapper import vector_space_mapper
from sklearn.feature_extraction.text import TfidfVectorizer


def obtain_score_for_lists(l1, l2, func):
    """Obtain comparison score for each element in the list."""
    scores = [
        func(word1, word2) for word1, word2 in itertools.product(
            l1, l2
        ) if func(word1, word2) is not None
    ]
    return sum(scores) / len(scores)


def get_cmp_func(model_1, model_2, bilingual_dict, cross_lingual=True):
    """Return the comparison function based on cross_lingual or not."""
    if cross_lingual is True:
        vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
        vm.map_vector_spaces()
        func = vm.obtain_cosine_similarity
    else:

        def func(word1, word2):
            try:
                return model_1.similarity(word1, word2)
            except KeyError:
                return None

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


def top_words(scores, words, n=5):
    """Return top n words using tf-idf."""
    l = {word: score for word, score in zip(words, scores)}
    return sorted(l, key=l.__getitem__)[:n]


if __name__ == '__main__':
    cmp_func = get_cmp_func(**_load_models(cross_lingual=False))
    tf1 = TfidfVectorizer(input="file", min_df=1, stop_words='english')
    tfidf_matrix1 = tf1.fit_transform([
        codecs.open(os.path.join(
            'data', 'blogs', 'gizmodu_3'
        ), 'r', encoding='utf-8'),
        codecs.open(os.path.join(
            'data', 'blogs', 'gizmodu_4'
        ), 'r', encoding='utf-8'),
        codecs.open(os.path.join(
            'data', 'blogs', 'gizmodu_5'
        ), 'r', encoding='utf-8')
    ])
    dense_mat1 = tfidf_matrix1.todense().tolist()
    tf2 = TfidfVectorizer(input="file", min_df=1, stop_words='english')
    tfidf_matrix2 = tf2.fit_transform([
        codecs.open(os.path.join(
            'data', 'blogs', 'gizmodu_1'
        ), 'r', encoding='utf-8'),
        codecs.open(os.path.join(
            'data', 'blogs', 'gizmodu_2'
        ), 'r', encoding='utf-8'),
    ])
    dense_mat2 = tfidf_matrix2.todense().tolist()
    for l1, l2 in itertools.product(dense_mat1, dense_mat2):
        words1 = top_words(l1, tf1.get_feature_names())
        words2 = top_words(l2, tf2.get_feature_names())
        print obtain_score_for_lists(words1, words2, cmp_func)
