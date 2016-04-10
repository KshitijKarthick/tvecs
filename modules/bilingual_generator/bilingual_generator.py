#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
**Module used to generate bilingual dictionary.**

- Utilise Yandex API for bilingual dictionary generation.
"""

import os
import codecs
import json
from gensim.models import Word2Vec
import random
from modules.preprocessor import yandex_api as yandex

def create_bilingual_dictionary(clusters_file_path, sample_size, model):
    """
    Create bilingual dictionary utilising Yandex, cluster file.

    **API Documentation**
        :param clusters_file_path: JSON cluster file.
        :param sample_size: The sample size of words in every cluster.
        :param model: Model in which the translation needs to exist.
        :type clusters_file_path: String
        :type sample_size: Integer
        :type model: :class:`gensim.models.Word2Vec`
        :return: Bilingual Dictionary generated from the cluster file.
        :rtype: List

    .. seealso::
        * :mod:`modules.bilingual_generator.clsutering`
        * :mod:`modules.preprocessor.yandex_api`
    """
    bilingual_dictionary = []
    with codecs.open(cluster_groups, 'r', encoding='utf-8') as file:
        clusters = json.load(file)
        for cluster in clusters:
            no_of_words = 0
            if len(cluster) >= sample_size:
                selected_words = set()
                count = 0
                while no_of_words < sample_size:
                    word = random.choice(cluster)
                    if count == len(cluster):
                        raise ValueError('No Valid words obtained')
                    if word not in selected_words:
                        count += 1
                        tr = yandex.get_valid_translation(word)
                        if tr is not None:
                            try:
                                model[tr]
                                selected_words.add(word)
                                bilingual_dictionary.append((word, tr))
                                no_of_words += 1
                            except:
                                print "Not Valid"
            else:
                raise ValueError("Sample Size too small")
    return bilingual_dictionary


if __name__ == '__main__':

    model = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-hindi-model')
    )

    cluster_groups=os.path.join(
        'data', 'vectors', 'english_clusters.json'
    )

    bilingual_dictionary = create_bilingual_dictionary(cluster_groups,1,model)

    bilingual_dict_path=os.path.join(
        'data', 'bilingual_dictionary', 'english_hindi_new.txt'
    )

    file = codecs.open(bilingual_dict_path, 'w', encoding='utf-8')
    for tup in bilingual_dictionary:
        file.write(tup[0]+ " " + tup[1] + "\n")