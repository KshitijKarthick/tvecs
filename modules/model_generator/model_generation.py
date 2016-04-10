#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
**Used to generate Word2Vec Models for individual languages after preprocessing.**

- Preprocessing Corpus - Implementation of BasePreprocessor module
    - HcCorpusPreprocessor
- Word2Vec Model Building
    - Gensim Word2Vec SkipGram implementation
"""

import os
import gensim
from modules.preprocessor import hccorpus_preprocessor as pre


def generate_model(
    language,
    corpus_fname,
    corpus_dir_path='.',
    output_dir_path=os.path.join('data', 'models'),
    need_preprocessing=True,
    iter=5
):
    """
    **Function used to preprocess and generate models.**

    **API Documentation**
        :param language: Language for which model is generated [ Used for model filename ]
        :type language: String
        :param corpus_fname: Corpus Filename
        :type corpus_fname: String
        :param corpus_dir_path: Directory Path where corpus exists [ Default current directory ]
        :type corpus_dir_path: String
        :param output_dir_path: Output Dir Path where model is stored
        :type output_dir_path: String
        :param need_preprocessing: Runs Preprocess with the same flag [ Default True ]
        :type need_preprocessing: Boolean [ True/False ]
        :param iter: Number of iterations for Word2Vec.
        :type iter: Integer
        :return: Constructed Model based on the provided specifications.
        :rtype: :mod:`gensim.models.Word2Vec`

    """
    preprocessor_obj = pre.HcCorpusPreprocessor(
        corpus_fname=corpus_fname,
        corpus_dir_path=corpus_dir_path,
        need_preprocessing=True,
        language=language
    )
    return construct_model(preprocessor_obj, iter)


def construct_model(
    preprocessed_corpus,
    language,
    output_dir_path=".",
    output_fname=None,
    iter=5
):
    """
    **Construct Model given the preprocessed corpus.**

    **API Documentation:**
        :param preprocessed_corpus: - (object)  - Instance of SubClass of BasePreprocessor
        :param language:           - (string)  - Language for which model is generated [ Used for model filename ]
        :param output_dir_path:    - (string)  - Output Dir Path where model is stored
        :param need_preprocessing: - (boolean) - Runs Preprocess with the same flag [ Default True ]
        :param iter:               - (number)  - Number of iterations for Word2Vec
        :return: Constructed Model based on the provided specifications.
        :rtype: :mod:`gensim.models.Word2Vec`

    .. seealso::
        * :mod:`gensim.models.Word2Vec`
        * :mod:`modules.preprocessor.hccorpus_preprocessor`
    """
    model = gensim.models.Word2Vec(preprocessed_corpus, iter=iter)
    if os.path.exists(output_dir_path) is False:
        os.makedirs(output_dir_path)
    if output_fname is None:
        output_path = os.path.join(
            output_dir_path, 't-vex-%s-model' % (language)
        )
    else:
        output_path = os.path.join(output_dir_path, output_fname)
    model.save(output_path)
    print("Model saved at %s" % (output_path))
    return model


if __name__ == '__main__':
    generate_model(
        language='hindi',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'Hindi'),
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='kannada',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'Kannada'),
        need_preprocessing=True,
        iter=5,
    )
    generate_model(
        language='tamil',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'Tamil'),
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='english',
        corpus_fname='all.txt',
        corpus_dir_path=os.path.join('data', 'corpus', 'English'),
        need_preprocessing=True,
        iter=5
    )
