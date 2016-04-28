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
from modules.logger import init_logger as log
from modules.model_generator import model_generation as model
from modules.preprocessor import emille_preprocessor as emilleprep
from modules.preprocessor import hccorpus_preprocessor as hcprep
from modules.preprocessor import leipzig_preprocessor as leipprep
from modules.vector_space_mapper import vector_space_mapper as vm
from modules.bilingual_generator import bilingual_generator as bg


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


def bilingual_generator(lang1, lang2):
    """Load & returns previously generated bilingual dictionary."""
    bilingual_dict = bg.load_bilingual_dictionary(
        os.path.join(
            'data', 'bilingual_dictionary', '%s_%s_train_bd' % (lang1, lang2)
        )
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
    return (
        lang1,
        lang2,
        model1,
        model2,
        corpus1,
        corpus2,
        iterations,
        silent,
        verbose
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
        help="Language name of model 1/ text 1",
        action="store"
    )
    parser.add_argument(
        "-l2",
        "--l2",
        dest="language2",
        help="Language name of model 2/ text 2",
        action="store"
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="config file path",
        action="store"
    )
    args = parser.parse_args()
    logger = log.initialise('T-Vecs')
    log.set_logger_normal(logger)
    parse_success = True
    try:
        # if Config is given higher priority, cmd line args are overriden
        if args.config:
            (
                args.language1, args.language2,
                args.model1, args.model2,
                args.corpus1, args.corpus2,
                args.iter, args.silent, args.verbose
            ) = parse_config(args.config)

        if args.verbose is True:
            log.set_logger_verbose(logger)

        elif args.silent is True:
            log.set_logger_silent(logger)

        # Load a precomputed model for trsl
        elif args.model1 and args.model2 and args.language1 and args.language2:
            order_of_evaluation = order_of_tvex_calls[2:]
            tvex_calls['model_generator']['result'] = (
                Word2Vec.load(args.model1),
                Word2Vec.load(args.model2)
            )

        # Build trsl using precomputed word sets and a config file
        elif args.corpus1 and args.corpus2:
            order_of_evaluation = order_of_tvex_calls[:]

        else:
            parse_success = False

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
    vm = tvex_calls['vector_space_mapper']['result']
    logger.info(
        "Avg Similarity Test Score :%s" % vm.obtain_avg_similarity_from_test(
            test_path=os.path.join(
                'data', 'bilingual_dictionary', 'english_hindi_test_bd'
            )
        )
    )
    new_time = time.time()
    loading_time = new_time - old_time
    logger.info("Execution Time :" + str(loading_time))


def evaluate(logger, args):
    """Evaluate and run sequence of operations based on user specs."""
    global tvex_calls, order_of_evaluation
    for func_name in order_of_evaluation:
        func = tvex_calls[func_name]['func']
        if func_name is "preprocessor":
            def preprocess_multiple_corpora(corpus_list, language):
                res = []
                for corpus in corpus_list:
                    fpath = corpus.keys()[0]
                    preprocessor_type = corpus.values()[0]
                    fname = ntpath.split(fpath)[1]
                    logger.info("Preprocessing %s\t=> %s" % (language, fpath))
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
                preprocess_multiple_corpora(
                    corpus_list=args.corpus1, language=args.language1
                ),
                preprocess_multiple_corpora(
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
                lang1=args.language1, lang2=args.language2
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
