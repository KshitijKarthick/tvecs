"""Test."""
import os
import json
import codecs
from sklearn.cluster import AffinityPropagation

from tvecs.logger import init_logger as log

LOGGER = log.initialise('T-Vecs.Clustering')


def build_clusters(entire_word_list, model, damping_factor=0.5):
    """
    Cluster word_list using Affinity Propagation.

    - Clustering based on the vectors from the Word2Vec model.

    API Documentation:
        :param entire_word_list: Word List provided to cluster.
        :param model:  Model to obtain the vectors for the word_list.
        :param damping_factor: Damping factor for the affinity propagation.
        :type entire_word_list: :class:`List`
        :type model: :mod:`gensim.models.Word2Vec`
        :type damping_factor: :class:`Float`
    """
    vocab = set(entire_word_list)
    d = {}
    for word in vocab:
        try:
            d[word] = model[word]
        except KeyError:
            pass
    word_list = d.keys()
    vector_list = d.values()
    LOGGER.info(
        'Clustering Using AffinityPropagation'
        'with %s Damping Factor', damping_factor
    )
    af = AffinityPropagation(damping=damping_factor).fit_predict(vector_list)
    clusters = [[] for x in word_list]
    for i, word in enumerate(word_list):
        clusters[af[i]].append(word)
    clusters = [
        cluster for cluster in clusters if len(cluster) > 0
    ]
    LOGGER.info(
        'Generated %s number of clusters', len(clusters)
    )
    return clusters


def write_clusters(
    word_list,
    model,
    encoding='utf-8',
    output_path=".",
    output_fname="clusters.json"
):
    """
    Write Clusters to the specified file as JSON.

    API Documentation:
        :param word_list: Word List provided to cluster.
        :param model: Model to obtain the vectors for the word_list.
        :param encoding: Encoding of the file written.
        :param output_fname: Filename of the output file.
        :param output_path: File path of the output file.
        :type word_list: :class:`List`
        :type model: :mod:`gensim.models.Word2Vec`
        :type encoding: :class:`String`
        :type output_fname: :class:`String`
        :type output_path: :class:`String`
    """
    clusters = build_clusters(entire_word_list=word_list, model=model)
    with codecs.open(
        os.path.join(output_path, output_fname), 'w', encoding=encoding
    ) as f:
        LOGGER.info(
            'Saving the clusters: %s', os.path.join(
                output_path, output_fname
            )
        )
        json.dump(clusters, f)

if __name__ == '__main__':
    log.set_logger_normal(LOGGER)
