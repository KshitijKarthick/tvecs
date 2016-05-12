#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
T-Vecs Driver Module.

Module used to control and coordinate all other modules for T-Vecs.
* Preprocessor
* Model Generation
* Bilingual Generation
* Vector Space Mapping
"""

import os
import time
import json
import ntpath
import argparse
import itertools as it
from gensim.models import Word2Vec

from logger import init_logger as log
from model_generator import model_generator as model
from preprocessor import emille_preprocessor as emilleprep
from preprocessor import hccorpus_preprocessor as hcprep
from preprocessor import leipzig_preprocessor as leipprep
from vector_space_mapper import vector_space_mapper as vm
from bilingual_generator import bilingual_generator as bg


def preprocess_corpus(*args, **kwargs):
    """Wrapper function for preprocessing module."""
    preprocessor_type = kwargs['preprocessor_type']
    del kwargs['preprocessor_type']
    data = []
    if preprocessor_type == hcprep.HcCorpusPreprocessor.__name__:
        data = hcprep.HcCorpusPreprocessor(*args, **kwargs)
    elif preprocessor_type == emilleprep.EmilleCorpusPreprocessor.__name__:
        data = emilleprep.EmilleCorpusPreprocessor(*args, **kwargs)
    elif preprocessor_type == leipprep.LeipzigPreprocessor.__name__:
        data = leipprep.LeipzigPreprocessor(*args, **kwargs)
    return data


def model_generator(
    preprocessed_corpus,
    language,
    output_dir_path=os.path.join(".", "data", "models"),
    iterations=5
):
    """
    Wrapper function for model_generator module.

    Function Arguments:
    * preprocessed_corpus - (HcCorpusPreprocessor) - Preprocessed corpus
    * language            - (string) - Language of Preprocessed corpus
    * output_dir_path     - (string) - Directory to store model [ Def: '.' ]
    * iter                - (int)    - No of iterations for model [ Def: 5 ]
    """
    return model.construct_model(
        preprocessed_corpus=preprocessed_corpus,
        language=language,
        output_dir_path=output_dir_path,
        iterations=iterations
    )


def bilingual_generator(lang1, lang2, bilingual_dict):
    """Load & returns previously generated bilingual dictionary."""
    bilingual_dict = bg.load_bilingual_dictionary(
        bilingual_dict
    )
    return bilingual_dict


def map_vector_spaces(*args, **kwargs):
    """Generate & return VectorSpaceMapper Instance and maps vectors spaces."""
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


def parse_config(config_path):
    """Used to load and parse config file."""
    config = json.load(open(config_path, 'r'))
    lang1_details = config.get('language1', {})
    lang1 = lang1_details.get('name', None)
    lang2_details = config.get('language2', {})
    lang2 = lang2_details.get('name', None)
    model1 = lang1_details.get('model', None)
    model2 = lang2_details.get('model', None)
    corpus1 = lang1_details.get('corpora')
    corpus2 = lang2_details.get('corpora')
    iterations = config.get('iterations', 5)
    silent = config.get('silent', False)
    verbose = config.get('verbose', False)
    bilingual_dict = config.get('bilingual_dict', '')
    return (
        lang1,
        lang2,
        model1,
        model2,
        corpus1,
        corpus2,
        iterations,
        silent,
        verbose,
        bilingual_dict
    )


def args_parser():
    """Utilised for cmdline arguments parsing."""
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
        help="number of Word2Vec iterations",
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
        help="language name of model 1/ text 1",
        action="store"
    )
    parser.add_argument(
        "-l2",
        "--l2",
        dest="language2",
        help="language name of model 2/ text 2",
        action="store"
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="config file path",
        action="store"
    )
    parser.add_argument(
        "-b",
        "--bilingual",
        dest="bilingual_dict",
        help="bilingual dictionary path",
        action="store"
    )
    parser.add_argument(
        "-r",
        "--recommendations",
        dest="recommendations",
        help="provide recommendations",
        action="store_true"
    )
    args = parser.parse_args()
    logger = log.initialise('TVecs')
    log.set_logger_normal(logger)
    parse_success = False
    try:
        # if Config is given higher priority, cmd line args are overriden
        if args.config:
            (
                args.language1, args.language2,
                args.model1, args.model2,
                args.corpus1, args.corpus2,
                args.iter, args.silent, args.verbose,
                args.bilingual_dict
            ) = parse_config(args.config)

        if args.verbose is True:
            log.set_logger_verbose(logger)

        elif args.silent is True:
            log.set_logger_silent(logger)

        valid_model = args.model1 and args.model2
        valid_lang = args.language1 and args.language2
        # Load a precomputed model for trsl
        if valid_model and valid_lang and args.bilingual_dict:
            logger.info(
                'Loading Model of %s :%s', args.language1, args.model1
            )
            model_1 = Word2Vec.load(args.model1)
            logger.info(
                'Loading Model of %s :%s', args.language2, args.model2
            )
            model_2 = Word2Vec.load(args.model2)
            order_of_evaluation = order_of_tvex_calls[2:]
            tvex_calls['model_generator']['result'] = (
                model_1,
                model_2
            )
            parse_success = True

        # Build trsl using precomputed word sets and a config file
        elif args.corpus1 and args.corpus2:
            order_of_evaluation = order_of_tvex_calls[:]
            parse_success = True

    except AttributeError:
        parse_success = False

    # Insufficient arguments passed to build trsl
    if parse_success is False:
        logger.error(
            "Required arguments not passed, run --help for more details"
        )
        return

    old_time = time.time()
    evaluate(logger, args)
    tvecs_vm = tvex_calls['vector_space_mapper']['result']
    logger.info(
        'Evaluation of Training Dataset'
    )
    tvecs_vm.obtain_mean_square_error_from_dataset(
        dataset_path=args.bilingual_dict
    )
    fpath, fname = ntpath.split(args.bilingual_dict)
    test_fname = fname.replace('train', 'test')
    if os.path.exists(os.path.join(fpath, test_fname)):
        logger.info(
            'Evaluation of Testing Dataset'
        )
        tvecs_vm.obtain_mean_square_error_from_dataset(
            dataset_path=os.path.join(fpath, fname)
        )
    new_time = time.time()
    loading_time = new_time - old_time
    logger.info("Execution Time: " + str(loading_time))
    if args.recommendations is True:
        logger.info(
            "Recommendation Engine: %s => %s" % (
                args.language1, args.language2
            )
        )
        while int(raw_input(
            '\nEnter your Choice:\n1> Recommendation\n2> Exit\n\nChoice: '
        )) == 1:
            word = raw_input(
                "\nEnter word in Language %s: " % args.language1
            )
            tvecs_vm.get_recommendations_from_word(
                word,
                pretty_print=True
            )


def evaluate(logger, args):
    """Evaluate and run sequence of operations based on user specs."""
    global tvex_calls, order_of_evaluation
    for func_name in order_of_evaluation:
        func = tvex_calls[func_name]['func']
        if func_name is "preprocessor":
            def _preprocess_multiple_corpora(corpus_list, language):
                res = []
                for corpus in corpus_list:
                    fpath = corpus.keys()[0]
                    preprocessor_type = corpus.values()[0]
                    fname = ntpath.split(fpath)[1]
                    logger.info("Preprocessing %s : %s", language, fpath)
                    res.append(
                        func(
                            corpus_fname=fname,
                            preprocessor_type=preprocessor_type,
                            corpus_dir_path=ntpath.split(fpath)[0],
                            encoding='utf-8',
                            need_preprocessing=True,
                            language=language
                        )
                    )
                return it.chain(*res)
            tvex_calls[func_name]['result'] = (
                _preprocess_multiple_corpora(
                    corpus_list=args.corpus1, language=args.language1
                ),
                _preprocess_multiple_corpora(
                    corpus_list=args.corpus2, language=args.language2
                )
            )
        elif func_name is "model_generator":
            tvex_calls[func_name]['result'] = (
                func(
                    preprocessed_corpus=tvex_calls[
                        "preprocessor"
                    ]["result"][0],
                    language=args.language1,
                    iterations=args.iter
                ),
                func(
                    preprocessed_corpus=tvex_calls[
                        "preprocessor"
                    ]["result"][1],
                    language=args.language2,
                    iterations=args.iter
                )
            )
        elif func_name is "bilingual_generator":
            tvex_calls[func_name]['result'] = func(
                lang1=args.language1,
                lang2=args.language2,
                bilingual_dict=args.bilingual_dict
            )
        elif func_name is "vector_space_mapper":
            tvex_calls[func_name]['result'] = func(
                model_1=tvex_calls["model_generator"]["result"][0],
                model_2=tvex_calls["model_generator"]["result"][1],
                bilingual_dict=tvex_calls["bilingual_generator"]["result"]
            )
        else:
            logger.error("Unknown Function!")


if __name__ == '__main__':
    args_parser()
