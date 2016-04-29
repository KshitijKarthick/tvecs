#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module used to generate bilingual dictionary."""

import os
import codecs

from modules.logger import init_logger as log


LOGGER = log.initialise('T-Vecs.BilingualDictionary')


def load_bilingual_dictionary(bilingual_dictionary_path, encoding='utf-8'):
    """
    Load bilingual dictionary.

    API Documentation
        :param bilingual_dictionary_path: Path for Bilingual Dictionary.
        :param encoding: Encoding of the bilingual dictionary.
        :type bilingual_dictionary_path: :fun:`str`
        :type encoding: :fun:`str`
        :return: Bilingual Dictionary loaded.
        :rtype: List

    .. seealso::
        * :mod:`modules.bilingual_generator.clustering`
        * :mod:`modules.preprocessor.yandex_api`
    """
    LOGGER.info(
        'Loading Bilingual Dictionary: %s' % bilingual_dictionary_path
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


if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    load_bilingual_dictionary(
        os.path.join(
            'data', 'bilingual_dictionary', 'english_hindi_train_bd'
        )
    )
