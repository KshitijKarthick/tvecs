"""
Used to generate Word2Vec Models for individual languages after preprocessing.

* Preprocessing Corpus - Implementation of BasePreprocessor module
    * HcCorpusPreprocessor
* Word2Vec Model Building
    * Gensim Word2Vec SkipGram implementation
"""

import os
import gensim
from hccorpus_preprocessor import HcCorpusPreprocessor


def generate_model(
    language,
    corpus_fname,
    corpus_dir_path='.',
    output_dir_path='./models',
    need_preprocessing=True,
    iter=5,
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
    preprocessor_obj = HcCorpusPreprocessor(
        corpus_fname=corpus_fname,
        corpus_dir_path=corpus_dir_path,
        need_preprocessing=True
    )
    model = gensim.models.Word2Vec(preprocessor_obj, iter=iter)
    output_fname = os.path.join(output_dir_path, 't-vex-%s-model' % (language))
    model.save(output_fname)
    print("Model saved at %s" % (output_fname))


if __name__ == '__main__':
    generate_model(
        language='hindi',
        corpus_fname='all.txt',
        corpus_dir_path='./corpus/Hindi',
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='kannada',
        corpus_fname='all.txt',
        corpus_dir_path='./corpus/Kannada',
        need_preprocessing=True,
        iter=5,
    )
    generate_model(
        language='tamil',
        corpus_fname='all.txt',
        corpus_dir_path='./corpus/Tamil',
        need_preprocessing=True,
        iter=5
    )
    generate_model(
        language='english',
        corpus_fname='all.txt',
        corpus_dir_path='./corpus/English',
        need_preprocessing=True,
        iter=5
    )
