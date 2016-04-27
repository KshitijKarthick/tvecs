#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to Perform tf-idf utilised for document similarity."""

import os
import glob
import codecs
import itertools
import numpy as np
import scipy
import json
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
    english_articles = glob.glob(
        os.path.join("data", "blogs", "English") + os.path.sep + "*.json"
    )
    hindi_articles = glob.glob(
        os.path.join("data", "blogs", "Hindi") + os.path.sep + "*.json"
    )
    z = {}
    sum = 0.0
    for ((l1, l2), (index1, index2)) in zip(
            itertools.product(
                english_articles, hindi_articles
            ), itertools.product(
                range(1, 21), range(1, 21)
            )
    ):
        cluster_list_1 = None
        cluster_list_2 = None
        with codecs.open(l1, 'r', encoding='utf-8') as article_1:
            cluster_list_1 = json.load(article_1)
        with codecs.open(l2, 'r', encoding='utf-8') as article_2:
            cluster_list_2 = json.loads(article_2.read())
        for cluster1, cluster2 in itertools.product(
            cluster_list_1, cluster_list_2
        ):
            word_vectors1 = []
            word_vectors2 = []

            for word in cluster1:
                try:
                    word_vectors1.append(tr(word))
                except:
                    pass

            for word in cluster2:
                try:
                    word_vectors2.append(kwargs['model_2'][word])
                except:
                    pass
            distance = scipy.spatial.distance.euclidean(
                np.mean(word_vectors1, axis=0),
                np.mean(word_vectors2, axis=0)
            )
            sum += distance
        z[
            (english_articles[index1 - 1], hindi_articles[index2 - 1])
        ] = sum / (len(cluster_list_1) * len(cluster_list_2))
        sum = 0.0

    l = sorted(z.items(), key=lambda (x, y): y, reverse=True)
    for x in l:
        print x
