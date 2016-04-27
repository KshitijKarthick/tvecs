"""Test."""
from sklearn.cluster import AffinityPropagation
from gensim.models import Word2Vec
import glob
import os
import json
import codecs


def cluster(words, model):
    """Test."""
    vocab = set(words)
    d = {}
    for word in vocab:
        try:
            d[word] = model[word]
        except KeyError:
            pass
    word_list = d.keys()
    vector_list = d.values()
    af = AffinityPropagation().fit_predict(vector_list)
    clusters = [[] for x in word_list]
    for i, word in enumerate(word_list):
        clusters[af[i]].append(word)
    return clusters


def write_clusters_for_articles(article_list, model):
    """Test."""
    for article in article_list:
        with codecs.open(article, 'r', encoding='utf-8') as fr:
            clustered_list = [
                l for l in cluster(
                    fr.read().lower().split(), model
                ) if len(l) > 1
            ]
            json.dump(clustered_list, codecs.open(
                article + ".json", 'w', encoding='utf-8'
            ))


if __name__ == '__main__':
    english_articles = glob.glob(os.path.join(
        'data',
        'blogs',
        'English'
    ) + os.path.sep + "*")
    hindi_articles = glob.glob(os.path.join(
        'data',
        'blogs',
        'Hindi'
    ) + os.path.sep + "*")
    model_1 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-english-model')
    )
    model_2 = Word2Vec.load(
        os.path.join('data', 'models', 't-vex-hindi-model')
    )
    write_clusters_for_articles(english_articles, model_1)
    write_clusters_for_articles(hindi_articles, model_2)
