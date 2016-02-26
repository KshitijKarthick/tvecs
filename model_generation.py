import os
import string
import codecs
import gensim
from nltk.tokenize import sent_tokenize


def preprocess_corpus(language, corpus_filename):
    print "Preprocessing %s corpus => %s" %(language, corpus_filename)
    corpus_data = codecs.open(corpus_filename, mode='r', encoding='utf-8').read()
    tab_split_list = corpus_data.split('\t')
    del(corpus_data)
    corpus_body_list = (
        tab_split_list[x] for x in range(len(tab_split_list)) if x%4==0 and x!=0 
    )
    corpus_body = " ".join(corpus_body_list)
    del(corpus_body_list)
    sent_split_list = sent_tokenize(corpus_body)
    del(corpus_body)
    intermediate = (
        (sentence.encode('utf-8').translate(None, string.punctuation)).decode('utf-8') for sentence in sent_split_list
    )
    del(sent_split_list)
    word_sent_split_list = [x.split() for x in intermediate]
    del(intermediate)
    return word_sent_split_list


def generate_model(language, corpus_filename, output_dir='./models', iter=5):
    word_sent_split_list = preprocess_corpus(language, corpus_filename)
    model = gensim.models.Word2Vec(word_sent_split_list, iter=iter)
    output_fname = os.path.join(output_dir, 't-vex-%s-model' %(language))
    model.save(output_fname)
    print "Model saved at %s" %(output_fname)


if __name__ == '__main__':
    generate_model('hindi', './corpus/Hindi/all.txt', iter=30)
    generate_model('kannada', './corpus/Kannada/all.txt', iter=30)
    generate_model('tamil', './corpus/Tamil/all.txt', iter=30)
    generate_model('english', './corpus/English/all.txt', iter=30)