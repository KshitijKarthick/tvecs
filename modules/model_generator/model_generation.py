"""
Used to generate Word2Vec Models for individual languages after preprocessing.

* Preprocessing Corpus - Implementation of BasePreprocessor module
    * HcCorpusPreprocessor
* Word2Vec Model Building
    * Gensim Word2Vec SkipGram implementation
"""

import os
import gensim
from modules.preprocessor import hccorpus_preprocessor as pre


def generate_model(
    language,
    corpus_fname,
    corpus_dir_path='.',
    output_dir_path='../data/models',
    need_preprocessing=True,
    iter=5
):
    """
    Function used to preprocess and generate models.

    Function Parameters:
    * language           - (string)  - Language for which model is generated
                                       [ Used for model filename ]
    * corpus_fname       - (string)  - Corpus Filename
    * corpus_dir_path    - (string)  - Directory Path where corpus exists
                                       [ Default current directory ]
    * output_dir_path    - (string)  - Output Dir Path where model is stored
    * need_preprocessing - (boolean) - Runs Preprocess with the same flag
                                       [ Default True ]
    * iter               - (number)  - Number of iterations for Word2Vec

    """
    preprocessor_obj = pre.HcCorpusPreprocessor(
        corpus_fname=corpus_fname,
        corpus_dir_path=corpus_dir_path,
        need_preprocessing=True
    )
    return construct_model(preprocessor_obj, iter)


def construct_model(
    preprocessed_corpus, language, output_dir_path=".", iter=5
):
    """Test."""
    model = gensim.models.Word2Vec(preprocessed_corpus, iter=iter)
    output_fname = os.path.join(output_dir_path, 't-vex-%s-model' % (language))
    model.save(output_fname)
    print("Model saved at %s" % (output_fname))
    return model


if __name__ == '__main__':
    generate_model(
        language='hindi',
        corpus_fname='all.txt',
        corpus_dir_path='../data/corpus/Hindi',
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='kannada',
        corpus_fname='all.txt',
        corpus_dir_path='../data/corpus/Kannada',
        need_preprocessing=True,
        iter=5,
    )
    generate_model(
        language='tamil',
        corpus_fname='all.txt',
        corpus_dir_path='../data/corpus/Tamil',
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='english',
        corpus_fname='all.txt',
        corpus_dir_path='../data/corpus/English',
        need_preprocessing=True,
        iter=5
    )
