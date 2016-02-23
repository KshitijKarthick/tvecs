import os
import codecs
import gensim
from nltk.tokenize import sent_tokenize


def preprocess_corpus(language, corpus_filename, output_dir='./models'):
    print "Preprocessing %s corpus => %s" %(language, corpus_filename)
    corpus_data = codecs.open(corpus_filename, mode='r', encoding='utf-8').read()
    tab_split_list = corpus_data.split('\t')
    corpus_body_list = [ 
        tab_split_list[x] for x in range(len(tab_split_list)) if x%4==0 and x!=0 
    ]
    corpus_body = " ".join(corpus_body_list)
    sent_split_list = sent_tokenize(corpus_body)
    word_sent_split_list = [x.split() for x in sent_split_list]
    model = gensim.models.Word2Vec(word_sent_split_list)
    output_fname = os.path.join(output_dir, 't-vex-%s-model' %(language))
    model.save(output_fname)
    print "Model saved at %s" %(output_fname)

if __name__ == '__main__':
    preprocess_corpus('hindi', './corpus/Hindi/all.txt')
    preprocess_corpus('kannada', './corpus/Kannada/all.txt')
    preprocess_corpus('tamil', './corpus/Tamil/all.txt')