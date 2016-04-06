#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Utilise Yandex Translation Service.

Obtain bilingual semantic human score.
"""

import os
import json
import codecs
import requests


def yandex_api(lang_translate, input_score_path, output_score_path):
    """
    Utilise Yandex Translation Service, obtain bilingual semantic human score.

    WordSim score, translated on one column using Yandex.
    Yandex Api Key, lang for translation needs to be provided
    """
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    options = {
        'lang': lang_translate,
        'key': '<Enter Key Here>'
    }
    output_data = []
    with codecs.open(input_score_path, 'r', encoding='utf-8') as file:
        with codecs.open(output_score_path, 'w', encoding='utf-8') as outfile:
            for line in file:
                word_1, word_2, score = line.split()
                options['text'] = word_2
                tr_word_2 = json.loads(
                    requests.get(base_url, params=options).text
                )["text"][0]
                try:
                    output_data.append("%s %s %s" % (
                        word_1,
                        tr_word_2,
                        score
                    ))
                except KeyError:
                    pass
            outfile.write("\n".join(output_data))


if __name__ == '__main__':
    dir_path = os.path.join(
        'data', 'evaluate'
    )
    datasets = [
        ('EN-MC-30.txt', dir_path),
        ('EN-RG-65.txt', dir_path),
        ('wordsim_relatedness_goldstandard.txt', dir_path),
        ('MEN_dataset_natural_form_full', dir_path),
        ('Mtruk.txt', dir_path)
    ]
    for (dataset_fname, dataset_dir) in datasets:
        print "Processing %s" %(dataset_fname)
        yandex_api(
            lang_translate='en-hi',
            input_score_path=os.path.join(
                dataset_dir, dataset_fname
            ),
            output_score_path=os.path.join(
                dataset_dir, '%s_translate' %(dataset_fname)
            )
        )
