"""
Utilise Yandex Translation Service.

Obtain bilingual semantic human score.
"""

import os
import json
import codecs
import requests
from gensim.models import Word2Vec
import modules.vector_space_mapper.vector_space_mapper as vsm


def yandex_api(lang_translate, input_score_path, output_score_path):
    """
    Utilise Yandex Translation Service, obtain bilingual semantic human score.

    WordSim score, translated on one column using Yandex.
    Yandex Api Key, lang for translation needs to be provided
    """
    vm = load_vector_space_mapper()
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    options = {
        'lang': lang_translate,
        'key': '<Enter Key Here>'
    }
    with codecs.open(input_score_path, 'r', encoding='utf-8') as file:
        with codecs.open(output_score_path, 'w', encoding='utf-8') as outfile:
            for line in file:
                word_1, word_2, score = line.split()
                options['text'] = word_2
                tr_word_2 = json.loads(
                    requests.get(base_url, params=options).text
                )["text"][0]
                try:
                    outfile.write("%s %s %s %s\n" % (
                        word_1,
                        tr_word_2,
                        score,
                        vm.obtain_cosine_similarity(word_1, tr_word_2)
                    ))
                except KeyError:
                    pass


def load_vector_space_mapper():
    """Generate Vector Space Mapper."""
    model_1 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    model_2 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-hindi-model')
    )
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
        vm = vsm.VectorSpaceMapper(model_1, model_2, bilingual_dict)
        vm.map_vector_spaces()
    return vm

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
