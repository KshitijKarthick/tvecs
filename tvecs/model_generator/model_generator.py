#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Used to generate Word2Vec Models for individual languages after preprocessing.

- Preprocessing Corpus - Implementation of BasePreprocessor module
    - HcCorpusPreprocessor

- Word2Vec Model Building
    - Gensim Word2Vec SkipGram implementation
"""
import os
import gensim

from tvecs.logger import init_logger as log
from tvecs.preprocessor.hccorpus_preprocessor import HcCorpusPreprocessor
from tvecs.preprocessor.emille_preprocessor import EmilleCorpusPreprocessor
from tvecs.preprocessor.leipzig_preprocessor import LeipzigPreprocessor

LOGGER = log.initialise('TVecs.ModelGeneration')


def generate_model(
        preprocessor_type,
        language,
        corpus_fname,
        corpus_dir_path='.',
        output_fname=None,
        output_dir_path=os.path.join('data', 'models'),
        need_preprocessing=True,
        iterations=5
):
    """
    Function used to preprocess and generate models.

    API Documentation
        :param preprocessor_type: Class Name for preprocessor.
        :type preprocessor_type: :class:`String`
        :param language: Language for which model is generated.
        :type language: :class:`String`
        :param corpus_fname: Corpus Filename
        :type corpus_fname: :class:`String`
        :param corpus_dir_path: Directory Path where corpus exists.
                                [ Default Current Directory ]
        :type corpus_dir_path: :class:`String`
        :param output_dir_path: Output Dir Path where model is stored
        :type output_dir_path: :class:`String`
        :param output_fname: Output filename to be generated.
        :type output_fname: :class:`String`
        :param need_preprocessing: Runs Preprocess with the same flag.
                                [ Default True ]
        :type need_preprocessing: :class:`Boolean`
        :param iterations: Number of iterations for Word2Vec.
                                [ Default value 5 ]
        :type iterations: :class:`Integer`
        :return: Constructed Model based on the provided specifications.
        :rtype: :mod:`gensim.models.Word2Vec`
    """
    LOGGER.info('Constructing Preprocessor Object')
    if preprocessor_type == HcCorpusPreprocessor.__name__:
        preprocessor_cl = HcCorpusPreprocessor
    elif preprocessor_type == LeipzigPreprocessor.__name__:
        preprocessor_type = LeipzigPreprocessor
    elif preprocessor_type == EmilleCorpusPreprocessor.__name__:
        preprocessor_type = EmilleCorpusPreprocessor
    else:
        raise ValueError("Invalid Preprocessor Type")
    preprocessor_obj = preprocessor_cl(
        corpus_fname=corpus_fname,
        corpus_dir_path=corpus_dir_path,
        need_preprocessing=need_preprocessing,
        language=language
    )
    return construct_model(
        preprocessed_corpus=preprocessor_obj,
        language=language,
        output_dir_path=output_dir_path,
        iterations=iterations,
        output_fname=output_fname
    )


def construct_model(
        preprocessed_corpus,
        language,
        output_dir_path=".",
        output_fname=None,
        iterations=5
):
    """
    Construct Model given the preprocessed corpus.

    API Documentation:
        :param preprocessed_corpus: Instance of SubClass of BasePreprocessor.
        :type preprocessed_corpus:
            Any class that inherits
            from :class:`tvecs.preprocessor.base_preprocessor`
        :param language: Language for which model is generated.
        :type language: :class:`String`
        :param output_dir_path: Output Dir Path where model is stored.
                                [ Default Current Directory ]
        :type output_dir_path: :class:`String`
        :param output_fname: Output file name set.
        :type output_fname: :class:`String`
        :param iterations: Number of iterations for Word2Vec.
                                [ Default value 5 ]
        :type iterations: :class:`Integer`
        :return: Constructed Model based on the provided specifications.
        :rtype: :mod:`gensim.models.Word2Vec`

    .. seealso::
        * :mod:`gensim.models.Word2Vec`
        * :mod:`tvecs.preprocessor.base_preprocessor`
    """
    LOGGER.info('Generating Model')
    model = gensim.models.Word2Vec(preprocessed_corpus, iter=iterations)
    if os.path.exists(output_dir_path) is False:
        os.makedirs(output_dir_path)
    if output_fname is None:
        output_path = os.path.join(
            output_dir_path, 't-vex-%s-model' % language
        )
    else:
        output_path = os.path.join(output_dir_path, output_fname)
    model.save(output_path)
    LOGGER.info("Model saved at %s", output_path)
    return model


if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    generate_model(
        language='hindi',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'Hindi'),
        need_preprocessing=True,
        iterations=5
    )
    generate_model(
        language='english',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'English'),
        need_preprocessing=True,
        iterations=5
    )
