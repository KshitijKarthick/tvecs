"""
Perform Multivariate Analysis.

Variables considered:
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


def evaluate(vsm):
    """Extract Correlation, P-Value for specified vector space mapper."""
    with codecs.open(os.path.join(
        'data', 'evaluate', 'wordsim_relatedness_translate.txt'
    ), 'r', encoding='utf-8') as file:
            human_score, calculated_score = zip(*[
                [data.split()[2], vsm.obtain_cosine_similarity(
                    data.split()[0], data.split()[1])]
                for data in file.readlines()
            ])
            human_score, calculated_score = zip(*[[
                float(hs), float(cs)
            ] for hs, cs in zip(
                human_score, calculated_score
            ) if hs is not None and cs is not None])
            return evaluation.get_correlation_coefficient(
                list(human_score), list(calculated_score)
            )


def multivariate_analyse():
    """Perform multivariate analysis."""
    corpus_size = [23887762, 35831643, 47775524, 59719405]
    bilingual_size = [706, 1060, 1413, 1766]
    with open(os.path.join(
        'data', 'multivariate', 'multivariate.csv'
    ), 'w+') as csvfile:
        fieldnames = [
            'corpus_size', 'bilingual_size',
            'correlation_score', 'p_value', 'execution_time'
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
                            limit=corpus
                        ),
                        language='hindi',
                        output_dir_path=m_2_path,
                        output_fname=m_2_fname
                    )
                else:
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
                        bilingual_dict=bilingual_dict
                    )
                    vsm.map_vector_spaces()
                    new_time = time.time()
                    correlation_score, p_value = evaluate(vsm)
                    writer.writerow({
                        'corpus_size': corpus,
                        'bilingual_size': bilingual,
                        'correlation_score': correlation_score,
                        'p_value': p_value,
                        'execution_time': (new_time - old_time) + m_exec_time
                    })


if __name__ == '__main__':
    multivariate_analyse()
