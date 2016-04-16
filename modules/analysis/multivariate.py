#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Perform Multivariate Analysis.

* Variables considered:
    * Corpus Size
    * Bilingual Dictionary Size
    * Execution time
    * Correlation Coefficient
    * P Value
"""

import os
import csv
import time
import codecs
from modules.preprocessor.hccorpus_preprocessor import HcCorpusPreprocessor
from modules.model_generator import model_generation
from modules.vector_space_mapper.vector_space_mapper import VectorSpaceMapper
from modules.evaluation import evaluation


def evaluate(vsm, wordsim_dataset_path):
    """Extract Correlation, P-Value for specified vector space mapper."""

    return evaluation.extract_correlation_coefficient(
            score_data_path=wordsim_dataset_path,
            vsm=vsm
    )


def multivariate_analyse():
    """Perform multivariate analysis."""
    corpus_size = [30607384, 45911076, 61214768, 76518461]
    bilingual_size = [4516, 6774, 9032, 11291]
    dir_path = os.path.join(
        'data', 'evaluate'
    )
    wordsim_datasets = [
        ('EN-MC-30.txt_translate', dir_path),
        ('EN-RG-65.txt_translate', dir_path),
        ('wordsim_relatedness_goldstandard.txt_translate', dir_path),
        ('MEN_dataset_natural_form_full_translate', dir_path),
        ('Mtruk.txt_translate', dir_path)
    ]
    with open(os.path.join(
        'data', 'multivariate', 'multivariate.csv'
    ), 'w+') as csvfile:
        fieldnames = [
            'corpus_size', 'bilingual_size', 'avg_sim_test', 'wordsim_dataset',
            'correlation_score', 'p_value', 'exec_time'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
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

            for corpus in corpus_size:
                m_old_time = time.time()
                m_1_fname = "%s-%s-models" % ('english', corpus)
                m_1_path = os.path.join('data', 'multivariate', 'models')
                m_2_fname = "%s-%s-models" % ('hindi', corpus)
                m_2_path = os.path.join('data', 'multivariate', 'models')
                if not os.path.exists(os.path.join(m_1_path, m_1_fname)):
                    model_1 = model_generation.construct_model(
                        HcCorpusPreprocessor(
                            corpus_fname='all.txt',
                            corpus_dir_path=os.path.join(
                                'data', 'corpus', 'English'
                            ),
                            need_preprocessing=True,
                            limit=corpus
                        ),
                        language='english',
                        output_dir_path=m_1_path,
                        output_fname=m_1_fname
                    )
                else:
                    if not os.path.exists(os.path.join(m_1_path)):
                        os.makedirs(directory)
                    model_1 =  model_generation.gensim.models.Word2Vec.load(
                        os.path.join(m_1_path, m_1_fname)
                    )
                if not os.path.exists(os.path.join(m_2_path, m_2_fname)):
                    model_2 = model_generation.construct_model(
                        HcCorpusPreprocessor(
                            corpus_fname='all.txt',
                            corpus_dir_path=os.path.join(
                                'data', 'corpus', 'Hindi'
                            ),
                            need_preprocessing=True,
                            language='hindi',
                            limit=corpus
                        ),
                        language='hindi',
                        output_dir_path=m_2_path,
                        output_fname=m_2_fname
                    )
                else:
                    if not os.path.exists(os.path.join(m_1_path)):
                        os.makedirs(directory)
                    model_2 =  model_generation.gensim.models.Word2Vec.load(
                        os.path.join(m_2_path, m_2_fname)
                    )
                m_exec_time = time.time() - m_old_time
                for bilingual in bilingual_size:
                    print("Corpus: %s Bilingual Size: %s" % (
                        corpus, bilingual
                    ))
                    old_time = time.time()
                    vsm = VectorSpaceMapper(
                        model_1=model_1,
                        model_2=model_2,
                        bilingual_dict=bilingual_dict[:bilingual]
                    )
                    vsm.map_vector_spaces()
                    new_time = time.time()
                    for index, (wordsim_fname, wordsim_dir) in enumerate(wordsim_datasets):
                        correlation_score, p_value = evaluate(
                            vsm=vsm,
                            wordsim_dataset_path=os.path.join(wordsim_dir, wordsim_fname)
                        )
                        writer.writerow({
                            'corpus_size': corpus,
                            'bilingual_size': bilingual,
                            'avg_sim_test': (
                                vsm.obtain_avg_similarity_from_test(
                                    test_path = os.path.join(
                                        'data',
                                        'bilingual_dictionary',
                                        'english_hindi_test_bd'
                                    )
                                )
                            ),
                            'wordsim_dataset': index,
                            'correlation_score': correlation_score,
                            'p_value': p_value,
                            'exec_time': (
                                new_time - old_time
                            ) + m_exec_time
                        })


if __name__ == '__main__':
    multivariate_analyse()
