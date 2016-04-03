#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Test."""

import os
import time
import codecs
import logging
import ntpath
import argparse
from gensim.models import Word2Vec
from modules.preprocessor import hccorpus_preprocessor as prep
from modules.model_generator import model_generation as model
from modules.vector_space_mapper import vector_space_mapper as vm


def preprocess_corpus(*args, **kwargs):
    """Test."""
    return prep.HcCorpusPreprocessor(*args, **kwargs)


def model_generator(
    preprocessed_corpus,
    language,
    output_dir_path=os.path.join(".", "data", "models"),
    iter=5
):
    """test."""
    return model.construct_model(
        preprocessed_corpus=preprocessed_corpus,
        language=language,
        output_dir_path=output_dir_path,
        iter=iter
    )


def bilingual_generator(lang1, lang2):
    """test."""
    bilingual_dict = []
    with codecs.open(
        os.path.join(
            'data', 'bilingual_dictionary', '%s_%s_train_bd' %(lang1, lang2)
        ), 'r',
        encoding='utf-8'
    ) as file:
        data = file.read().split('\n')
        bilingual_dict = [
            (line.split(' ')[0], line.split(' ')[1])
            for line in data
        ]
    return bilingual_dict


def map_vector_spaces(*args, **kwargs):
    """test."""
    vector_mapper_obj = vm.VectorSpaceMapper(*args, **kwargs)
    vector_mapper_obj.map_vector_spaces()
    return vector_mapper_obj


tvex_calls = {
    'preprocessor': {
        'func': preprocess_corpus, 'result': None
    },
    'model_generator': {
        'func': model_generator, 'result': None
    },
    'bilingual_generator': {
        'func': bilingual_generator, 'result': None
    },
    'vector_space_mapper': {
        'func': map_vector_spaces, 'result': None
    },
}
order_of_tvex_calls = [
    'preprocessor',
    'model_generator',
    'bilingual_generator',
    'vector_space_mapper'
]

order_of_evaluation = order_of_tvex_calls[:]


def args_parser():
    """Initialise the format and level of the logging."""
    global order_of_tvex_calls, order_of_evaluation
    parser = argparse.ArgumentParser(
        description='Script used to generate models'
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    parser.add_argument(
        "-s",
        "--silent",
        help="silence all logging",
        action="store_true"
    )
    parser.add_argument(
        "-i",
        "--iter",
        help="number of word2vec iter",
        default=5,
        action="store"
    )
    parser.add_argument(
        "-m1",
        "--model1",
        dest="model1",
        help="pre-computed model file path",
        action="store"
    )
    parser.add_argument(
        "-m2",
        "--model2",
        dest="model2",
        help="pre-computed model file path",
        action="store"
    )
    parser.add_argument(
        "-l1",
        "--language1",
        dest="language1",
        required=True,
        help="Language name of model 1/ text 1",
        action="store"
    )
    parser.add_argument(
        "-l2",
        "--l2",
        dest="language2",
        required=True,
        help="Language name of model 2/ text 2",
        action="store"
    )
    parser.add_argument(
        "-t1",
        "--text1",
        dest="corpus1",
        help="text corpus for model generation",
        action="store"
    )
    parser.add_argument(
        "-t2",
        "--text2",
        dest="corpus2",
        help="text corpus for model generation",
        action="store"
    )
    args = parser.parse_args()
    logger = init_logger(args)
    # Load a precomputed model for trsl
    if args.model1 and args.model2:
        order_of_evaluation = order_of_tvex_calls[2:]
        tvex_calls['model_generator']['result'] = (
            Word2Vec.load(args.model1),
            Word2Vec.load(args.model2)
        )
    # Build trsl using precomputed word sets and a config file
    elif args.corpus1 and args.corpus2:
        order_of_evaluation = order_of_tvex_calls[:]
    # Insufficient arguments passed to build trsl
    else:
        logger.error(
            "Required arguments not passed, run --help for more details"
        )
        return

    old_time = time.time()
    evaluate(logger, args)
    new_time = time.time()
    loading_time = new_time - old_time
    logger.info("Execution Time : " + str(loading_time))


def init_logger(args):
    """Initialise the logger based on user preference."""
    logging.basicConfig()
    logger = logging.getLogger('T-Vecs')
    if args.silent:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


def evaluate(logger, args):
    """test."""
    global tvex_calls, order_of_evaluation
    for func_name in order_of_evaluation:
        func = tvex_calls[func_name]['func']
        if func_name is "preprocessor":
            fname_1 = ntpath.split(args.corpus1)[1]
            fname_2 = ntpath.split(args.corpus2)[1]
            logger.info("Preprocessing %s %s:" % (args.corpus1, args.corpus2))
            tvex_calls[func_name]['result'] = (
                func(
                    corpus_fname=fname_1,
                    corpus_dir_path=ntpath.split(args.corpus1)[0],
                    encoding='utf-8',
                    need_preprocessing=True,
                    language=args.language1
                ),
                func(
                    corpus_fname=fname_2,
                    corpus_dir_path=ntpath.split(args.corpus2)[0],
                    encoding='utf-8',
                    need_preprocessing=True,
                    language=args.language2
                )
            )
        elif func_name is "model_generator":
            logger.info("Model Generation")
            tvex_calls[func_name]['result'] = (
                func(
                    preprocessed_corpus=tvex_calls[
                        "preprocessor"
                    ]["result"][0],
                    language=args.language1,
                    iter=args.iter
                ),
                func(
                    preprocessed_corpus=tvex_calls[
                        "preprocessor"
                    ]["result"][1],
                    language=args.language2,
                    iter=args.iter
                )
            )
        elif func_name is "bilingual_generator":
            logger.info("Running Bilingual Generator")
            tvex_calls[func_name]['result'] = func(
                lang1=args.language1, lang2=args.language2
            )
        elif func_name is "vector_space_mapper":
            logger.info("Mapping Vector Spaces Together")
            tvex_calls[func_name]['result'] = func(
                model_1=tvex_calls["model_generator"]["result"][0],
                model_2=tvex_calls["model_generator"]["result"][1],
                bilingual_dict=tvex_calls["bilingual_generator"]["result"]
            )
        else:
            logger.error("Unknown Function!")


if __name__ == '__main__':
    args_parser()
