#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to Evaluate T-Vecs model against Human Semantic Similarity Score."""
import os
import codecs
from scipy.stats import pearsonr
from gensim.models import Word2Vec

from modules.logger import init_logger as log
from modules.bilingual_generator import bilingual_generator as bg
from modules.vector_space_mapper.vector_space_mapper import VectorSpaceMapper

LOGGER = log.initialise('T-Vecs.Evaluation')


def extract_correlation_coefficient(score_data_path, vsm):
    """
    Extract Human Score, Word1, Word2. Compute T-Vecs Score.

    API Documentation
        :param score_data_path: File generated by preprocessor/yandex
        :param vsm: Vector spaces mapped using 2 models.
        :type score_data_path: String
        :type vsm: :mod:`modules.vector_space_mapper.vector_space_mapper`
        :return: Returns (Correlation coefficient, P-Value)
        :rtype: Tuple(Float, Float)
    """
    LOGGER.info(
        'Extracting Human Score from score data path: %s', score_data_path
    )
    with codecs.open(score_data_path, 'r', encoding='utf-8') as score_file:
        human_score, calculated_score = zip(*[
            [
                data.split()[2], vsm.obtain_cosine_similarity(
                    data.split()[0], data.split()[1]
                )
            ]
            for data in score_file.readlines()
        ])
        human_score, calculated_score = zip(*[[
            float(hs), float(cs)
        ] for hs, cs in zip(
            human_score, calculated_score
        ) if hs is not None and cs is not None])
        return get_correlation_coefficient(
            list(human_score), list(calculated_score)
        )


def get_correlation_coefficient(human_score, calculated_score):
    """
    Measure correlation using Pearson's Coefficient.

    - The correlation is between the T-Vecs Model and
    - Human Semantic Similarity Score.

    API Documentation:
        :param human_score: List of human scores.
        :param calculated_score: List of calculated scores.
        :type human_score: :class:`List`
        :type calculated_score: :class:`List`
        :return: (Correlation Coefficient, P-Value)
        :rtype: Tuple(Float, Float)

    .. note::
        * correlation_coefficient - Measure of degree of relatedness
          between two variables
        * p-value - The null hypothesis is that the
          two variables are uncorrelated. The p-value is a number between zero
          and one that represents the probability that your data would have
          arisen if the null hypothesis were true.

    .. seealso::
        * :mod:`scipy.stats`
    """
    LOGGER.info('Computing Correlation Coefficient b/w human, t-vecs score')
    return pearsonr(human_score, calculated_score)


def _load_vector_space_mapper(model_1_path, model_2_path, bilingual_path):
    """Build a vector space mapper from model 1,2 and bilingual dict."""
    model_1 = Word2Vec.load(model_1_path)
    model_2 = Word2Vec.load(model_2_path)
    bilingual_dict = bg.load_bilingual_dictionary(bilingual_path)
    tvecs_vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
    tvecs_vm.map_vector_spaces()
    return tvecs_vm

if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    LOGGER.info(
        "Evaluation of T-Vecs Model against Human Semantic Similarity Score:"
    )
    CORRELATION_SCORE, P_VALUE = extract_correlation_coefficient(
        score_data_path=os.path.join(
            'data', 'evaluate',
            'wordsim_relatedness_goldstandard.txt_translate'
        ),
        vsm=_load_vector_space_mapper(
            model_1_path=os.path.join('data', 'models', 't-vex-english-model'),
            model_2_path=os.path.join('data', 'models', 't-vex-hindi-model'),
            bilingual_path=os.path.join(
                'data', 'bilingual_dictionary', 'english_hindi_train_bd'
            )
        )
    )
    LOGGER.info(
        "Correlation Score obtained: %s\nP-Value obtained: %s",
        CORRELATION_SCORE, P_VALUE
    )
