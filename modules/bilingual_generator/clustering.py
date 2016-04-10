#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""**Module generates clusters from a Model.**"""

from sklearn.cluster import KMeans
from gensim.models import Word2Vec
import os
import cPickle
import codecs
import logging
import json
import numpy as np


def cluster(language, vec_list, word_list, num_clusters=1000, n_jobs=3):
    """
    **Utilised for clustering passed Vector List, and return n clusters.**

    **API Documentation:**
        :param language: Language utilised for filename for cluster file.
        :param vec_list: A vector list obtained from the Model.
        :param word_list: A word list obtained from the Model corresponding to vec_list.
        :param num_clusters: Num of clusters to be generated [ Default 1000 ]
        :param n_jobs: Num of jobs [ multiprocessing ]

    .. seealso::
        * :mod:`modules.model_generator.model_generation`
    """
    kmeans_clust = KMeans(
        n_clusters=num_clusters,
        precompute_distances=True,
        n_jobs=n_jobs,
    )
    idx = kmeans_clust.fit_predict(vec_list)
    k = [[] for _ in xrange(num_clusters)]
    word_centroid_map = dict(zip(word_list, idx))
    for word in word_centroid_map.keys():
        k[word_centroid_map[word]].append(word)
    with codecs.open(os.path.join(
        'data', 'vectors', '%s-%s-clustering.json' % (language, num_clusters)
    ), 'w', encoding='utf-8') as file:
        file.write(
            json.dumps(k)
        )

if __name__ == '__main__':
    language = 'english'
    num_clusters = 1000
    logging.basicConfig(level=logging.DEBUG)
    model = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    word_list = np.array(model.vocab.keys())
    vec_list = np.array([model[word] for word in word_list])
    del(model)
    with codecs.open(
        os.path.join(
            'data', 'vectors', '%s-%s-vectors' % (language, num_clusters)
        ), 'w'
    ) as file:
        file.write(
            cPickle.dumps({
                'vector_list': vec_list,
                'word_list': word_list,
            })
        )
    cluster(
        language=language,
        vec_list=vec_list,
        word_list=word_list,
        num_clusters=num_clusters
    )
