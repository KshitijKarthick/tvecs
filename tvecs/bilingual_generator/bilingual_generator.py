#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module used to generate bilingual dictionary."""

import os
import random
import codecs
from gensim.models import Word2Vec

from tvecs.bilingual_generator import cluster as cl
from tvecs.logger import init_logger as log


LOGGER = log.initialise('T-Vecs.BilingualDictionary')


def load_bilingual_dictionary(bilingual_dictionary_path, encoding='utf-8'):
    """
    Load bilingual dictionary from the specified bilingual_dictionary_path.

    API Documentation
        :param bilingual_dictionary_path: Path for Bilingual Dictionary.
        :param encoding: Encoding of the bilingual dictionary.
        :type bilingual_dictionary_path: :func:`str`
        :type encoding: str
        :return: Bilingual Dictionary loaded.
        :rtype: List
    """
    LOGGER.info(
        'Loading Bilingual Dictionary: %s', bilingual_dictionary_path
    )
    with codecs.open(
        bilingual_dictionary_path, 'r', encoding=encoding
    ) as f:
        data = f.read().split('\n')
        bilingual_dict = [
            (line.split(' ')[0], line.split(' ')[1])
            for line in data
        ]
    return bilingual_dict


def build_sparse_bilingual_dictionary(
        bilingual_dictionary_path,
        model,
        encoding='utf-8',
        output_path=os.path.join('data', 'bilingual_dictionary'),
        output_fname="sparse_bd",
        topn=5000,
        sample_size=1
):
    """
    Create Sparse Bilingual Dictionary.

    - Cluster pre-existing Bilingual Dictionary and sample from the same.

    API Documentation
        :param bilingual_dictionary_path: Path for Bilingual Dictionary.
        :param model: Word2Vec Model for obtaining vectors.
        :param encoding: Encoding of the bilingual dictionary.
        :param output_fname: Output Filename for sparse bilingual dictionary.
        :param output_path: Output file path for bilingual dictionary.
        :param topn: Number of words considered from bilingual dictionary.
        :param sample_size: Number of samples from each cluster.
        :type bilingual_dictionary_path: :func:`str`
        :type encoding: :func:`str`
        :type model: 'mod'`gensim.models.Word2Vec`.
        :type output_fname: str
        :type output_path: str
        :type topn: int
        :type sample_size: int

    .. seealso::
        * :mod:`modules.bilingual_generator.clustering`
    """
    LOGGER.info(
        'Building Bilingual Dictionary from: %s', bilingual_dictionary_path
    )
    bilingual_dict = dict(load_bilingual_dictionary(
        bilingual_dictionary_path=bilingual_dictionary_path,
        encoding=encoding
    ))
    word_list = bilingual_dict.keys()[:topn]
    clusters = cl.build_clusters(
        entire_word_list=word_list,
        model=model
    )
    subset_of_clusters = [
        random.sample(cluster, sample_size) for cluster in clusters
    ]
    sparse_bilingual_dict = "\n".join([
        "%s %s" % (
            word, bilingual_dict[word]
        ) for cluster in subset_of_clusters for word in cluster
    ])
    with codecs.open(
        os.path.join(output_path, output_fname), 'w', encoding=encoding
    ) as f:
        LOGGER.info(
            'Save the Bilingual Dictionary: %s', os.path.join(
                output_path, output_fname
            )
        )
        f.write(sparse_bilingual_dict)


if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    model = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    build_sparse_bilingual_dictionary(
        bilingual_dictionary_path=os.path.join(
            'data', 'bilingual_dictionary', 'english_hindi_train_bd'
        ),
        model=model,
    )
