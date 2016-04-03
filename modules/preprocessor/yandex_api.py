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

    yandex_api(
        lang_translate='en-hi',
        input_score_path=os.path.join(
            'data', 'evaluate', 'wordsim_relatedness_goldstandard.txt'
        ),
        output_score_path=os.path.join(
            'data', 'evaluate', 'wordsim_relatedness_translate.txt'
        )
    )
