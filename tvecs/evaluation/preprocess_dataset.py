#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Preprocess Evaluation Dataset by translating 1 column."""

import os
import codecs
from tvecs.logger import init_logger as log
from tvecs.preprocessor import yandex_api as yp

LOGGER = log.initialise('TVecs.Evaluation.Preprocess')


def preprocess_dataset(dataset_path, delimiter='', encoding='utf-8'):
    """Preprocess Evaluation dataset by preprocessing 1 column."""
    with codecs.open(dataset_path, 'r', encoding=encoding) as dataset_handle:
        LOGGER.info('Opening Evaluation Dataset for Preprocessing.')
        data = dataset_handle.read().split()
        output_data = []
        for line in data:
            word_1, word_2, score = line.split(
                delimiter
            )
            t_word = yp.get_translation(word_2, 'en-hi').split()
            if len(t_word) > 0:
                t_word = t_word[0]
                processed_data = "\t".join([word_1, t_word, score])
                LOGGER.debug(
                    '%s : %s' % (
                        'Preprocessed Evaluation Dataset',
                        preprocess_dataset
                    )
                )
                output_data.append(processed_data)
    with codecs.open(
        '%s_%s' % (dataset_path, 'translate'), 'w', encoding=encoding
    ) as output_handle:
        LOGGER.info('Writing Preprocessed Evaluation Dataset.')
        output_handle.write((os.linesep).join(output_data))


if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
    preprocess_dataset(
        dataset_path=os.path.join(
            'data', 'evaluate', 'MTURK-771.csv'
        ),
        delimiter=','
    )
