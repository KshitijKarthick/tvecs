#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""CherryPy Server to provide recommendations of semantic similarity."""

import os
import json
import codecs
import cherrypy
import argparse
import ConfigParser
from gensim.models import Word2Vec
from jinja2 import Environment, FileSystemLoader

from tvecs.preprocessor import yandex_api as yandex
from tvecs.vector_space_mapper.vector_space_mapper import VectorSpaceMapper


class Server(object):
    """
    Server Configuration for t-vex.

    .. seealso::
        * :mod:`cherrypy`
    """

    def __init__(self):
        """Initialization the Language and Model."""
        self.model = {
            'english': Server._load_model('english'),
            'hindi': Server._load_model('hindi')
        }
        self.cross_lang_vm = {
            ('english', 'hindi'): self._create_vector_space_mapper(
                'english', 'hindi'
            ),
            ('hindi', 'english'): self._create_vector_space_mapper(
                'hindi', 'english'
            )
        }
        self.cache_file_path = os.path.join(
            'tvecs', 'visualization', 'cached_dictionary'
        )
        if not os.path.exists(self.cache_file_path):
            json.dump({}, codecs.open(
                self.cache_file_path, 'w', encoding='utf-8'
            ))
            self.cached_dictionary = {}
        with codecs.open(self.cache_file_path, 'r', encoding='utf-8') as f:
            self.cached_dictionary = json.load(f)

    @cherrypy.expose
    def index(self):
        """Semantic spac visualization html returned."""
        return file(os.path.join(
            'tvecs', 'visualization', 'static', 'index.html'
        ))

    @cherrypy.expose
    def multivariate_analysis(self):
        """Parallel Coordinates for multivariate analysis html page return."""
        return file(os.path.join(
            'tvecs', 'visualization', 'static', 'multivariate.html')
        )

    @cherrypy.expose
    def cross_lingual(self):
        """Cross Lingual recommender html returned."""
        return file(os.path.join(
            'tvecs', 'visualization', 'static', 'cross_lingual.html')
        )

    @cherrypy.expose
    def distances(self):
        """Visualization with distances html returned."""
        return file(os.path.join(
            'tvecs', 'visualization', 'static', 'distances.html')
        )

    @cherrypy.expose
    def lingual_semantics(self):
        """Semantically related words in same language returned."""
        return file(os.path.join(
            'tvecs', 'visualization', 'static', 'intra_language.html')
        )

    def retrieve_meaning(self, language, word):
        """
        Optional: Translate the word.

        Retrieve Eng definition(s) of a word from cached file or PyDictionary.

        API Documentation
            :param language: Language for which definition needed
            :param word: Word whose definition needs to be retrieved

            :type language: String
            :type word: String

            :return: word and definition
            :rtype: :class:`String`

        """
        from PyDictionary import PyDictionary
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        word = word.lower()
        trword = word
        if word in self.cached_dictionary:
            return json.dumps(self.cached_dictionary[word])
        else:
            if language == 'hindi':
                trword = yandex.get_translation(word, "hi-en")

            dictionary = PyDictionary(trword)
            meanings = [trword, dictionary.meaning(trword)]
            if meanings[1]:
                self.cached_dictionary[word] = meanings
                with codecs.open(
                    self.cache_file_path, 'w', encoding='utf-8'
                ) as f:
                    f.write(json.dumps(self.cached_dictionary))
            return json.dumps(meanings)

    @cherrypy.expose
    def get_distance(self, word1, word2, language1, language2):
        """
        Retrieve cosine distance between word1 and word2.

        - word1 and word2 have to be in the vocabulary
          of language1 and language2, respectively.

        API Documentation
            :param word1: A word in language1's vocabulary
            :param language1: Language of word1
            :param word2: A word in language2's vocabulary
            :param language2: Language of word2
            :type word1: String
            :type language1: String
            :type word2: String
            :type language2: String
            :return: Dictionary with keys 'word1', 'word2', and 'distance'
            :rtype: :class:`Dictionary`

        .. py:currentmodule:: tvecs.vector_space_mapper.vector_space_mapper

        .. seealso::
            * :func:`VectorSpaceMapper.obtain_cosine_similarity`
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        word1 = word1.lower()
        word2 = word2.lower()
        vm = self.cross_lang_vm.get((language1, language2))
        similarity = None
        if vm is not None:
            similarity = vm.obtain_cosine_similarity(word1, word2)

        distance = 1 - similarity if similarity is not None else None
        return json.dumps(
            {
                'word1': word1,
                'word2': word2,
                'distance': distance
            }
        )

    @cherrypy.expose
    def retrieve_recommendations(self, language, word, limit=10):
        """
        Retrieve number of semantically similar recommendations.

        - For specified word in the given lang retrieve limit recommendations

        API Documentation
            :param language: Language for which recommendations required
            :param word: Semantic similar words provided for given word
            :param limit: No of words to be recommended [ Default 10 ]
            :type language: String
            :type word: String
            :type limit: Integer
            :return: List of recommendations
            :rtype: :class:`List`

        .. seealso::
            * :class:`gensim.models.Word2Vec`
        """
        word = word.lower()
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        model = self.model.get(language)
        if model is not None:
            data = Server._recommend(
                word, int(limit), fn=model.most_similar
            )
        else:
            data = json.dumps(None)
        return data

    @cherrypy.expose
    def get_cross_lingual_recommendations(
        self,
        lang1,
        lang2,
        word,
        topn=10
    ):
        """
        Provide cross lingual recommendations.

        API Documentation
            :param lang1: Language 1 for cross lingual recommendations.
            :param lang2: Language 2 for cross lingual recommendations.
            :param word: Word utilised for cross lingual recommendations.
            :param topn: No of recommendations provided.
            :type lang1: String
            :type lang2: String
            :type word: String
            :type topn: Integer
            :return: List of recommendations
            :rtype: :class:`List`

        .. seealso::
            * :mod:`tvecs.vector_space_mapper.vector_space_mapper`
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        word = word.lower()
        vm = self.cross_lang_vm.get((lang1, lang2))
        data = None
        if vm is not None:
            data = Server._recommend(
                word, int(topn), fn=vm.get_recommendations_from_word
            )
        return data

    @cherrypy.expose
    def _create_vector_space_mapper(self, lang1, lang2):
        """
        Create Vector Space Mapper between Languages.

        API Documentation
            :param lang1: Language 1 used for building
                :class:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper`
                object
            :param lang2: Language 2 used for building
                :class:`tvecs.vector_space_mapper.vector_space_mapper.VectorSpaceMapper`
                object
            :return: JSON with successful/failure message
            :rtype: JSON

        .. seealso::
            :mod:`tvecs.vector_space_mapper.vector_space_mapper`
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        vm = None
        with codecs.open(
            os.path.join(
                'data', 'bilingual_dictionary', '%s_%s_train_bd' % (
                    lang1, lang2
                )
            ), 'r', encoding='utf-8'
        ) as file:
            data = file.read().split('\n')
            bilingual_dict = [
                (line.split(' ')[0], line.split(' ')[1])
                for line in data
            ]
            if (self.model.get(lang1) is not None) and (
                self.model.get(lang2) is not None
            ):
                vm = VectorSpaceMapper(
                    self.model[lang1], self.model[lang2], bilingual_dict
                )
                vm.map_vector_spaces()
        return vm

    @staticmethod
    def _recommend(word, limit, fn):
        """Vector Space Mapper recommend functionality."""
        try:
            vec_list = fn(word, topn=limit)
        except KeyError:
            vec_list = None
        if vec_list is not None:
            data = json.dumps([
                {
                    'word': tup[0],
                    'weight': tup[1]
                } for tup in vec_list
            ])
        else:
            data = json.dumps(None)
        return data

    @staticmethod
    def _load_model(language):
        """Used to load Word2Vec Model."""
        return Word2Vec.load(
            os.path.join('data', 'models', 't-vex-%s-model' % language)
        )


if __name__ == '__main__':
    """Setting up the Server with Specified Configuration"""
    parser = argparse.ArgumentParser(
      description='Obtain Server Configuration'
    )
    parser.add_argument(
      '-c', '--config', dest='config',
      help='Config File Path', action='store', type=str,
      default=os.path.join('tvecs', 'visualization', 'server.conf')
    )
    parser.add_argument(
      '-p', '--port', dest='port',
      help='Port', action='store', type=int, default=None
    )
    parser.add_argument(
      '-s', '--host', dest='host',
      help='Host Name', action='store', type=str, default=None
    )
    args = parser.parse_args()
    server_config = ConfigParser.RawConfigParser()
    env = Environment(loader=FileSystemLoader('static'))
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'tvecs', 'visualization', 'static', 'js'
            )
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'tvecs', 'visualization', 'static', 'css'
            )
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'tvecs', 'visualization', 'static', 'images'
            )
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'tvecs', 'visualization', 'static', 'resources'
            )
        }
    }
    server_port = args.port
    server_host = args.host
    server_config.read(args.config)
    if args.port is None:
      server_port = server_config.get('Server', 'port')
    if args.host is None:
      server_host = server_config.get('Server', 'host')
    thread_pool = server_config.get('Server', 'thread_pool')
    queue_size = server_config.get('Server', 'queue_size')
    cherrypy.config.update({'server.socket_host': server_host})
    cherrypy.config.update({'server.thread_pool': int(thread_pool)})
    cherrypy.config.update({'server.socket_queue_size': int(queue_size)})
    cherrypy.config.update({'server.socket_port': int(
        os.environ.get('PORT', server_port)
    )})
    cherrypy.quickstart(Server(), '/', conf)
