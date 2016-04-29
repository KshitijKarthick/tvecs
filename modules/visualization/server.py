#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""CherryPy Server to provide recommendations of semantic similarity."""

import os
import json
import codecs
import cherrypy
import ConfigParser
from gensim.models import Word2Vec
from PyDictionary import PyDictionary
from jinja2 import Environment, FileSystemLoader
from modules.preprocessor import yandex_api as yandex
from modules.vector_space_mapper.vector_space_mapper import VectorSpaceMapper


class Server():
    """
    Server Configuration for t-vex.

    API Documentation:
        :param language: Language used for same space recommendations.
        :param cross_lang1: Language 1 used for cross lingual recommendations.
        :param cross_lang2: Language 2 used for cross lingual recommendations.
        :param vm: Vector Space Mapper between cross_lang1 and cross_lang2.
        :param model: Model loaded for lang param same space recommendations.

    .. seealso::
        * :mod:`cherrypy`
    """

    def __init__(self):
        """Initialization the Language and Model."""
        self.model = {
            'english': self._load_model('english'),
            'hindi': self._load_model('hindi')
        }
        self.cross_lang_vm = {
            ('english', 'hindi'): self._create_vector_space_mapper(
                'english', 'hindi'
            ),
            ('hindi', 'english'): self._create_vector_space_mapper(
                'hindi', 'english'
            )
        }
        cache_file_path = os.path.join(
            'modules', 'visualization', 'cached_dictionary'
        )
        if not os.path.exists(cache_file_path):
            json.dump({}, codecs.open(
                cache_file_path, 'w', encoding='utf-8'
            ))
            self.cached_dictionary = {}
        with codecs.open(cache_file_path, 'r', encoding='utf-8') as f:
            self.cached_dictionary = json.load(f)

    @cherrypy.expose
    def index(self):
        """Semantic spac visualization html returned."""
        return file(os.path.join(
            'modules', 'visualization', 'static', 'index.html'
        ))

    @cherrypy.expose
    def multivariate_analysis(self):
        """Parallel Coordinates for multivariate analysis html page return."""
        return file(os.path.join(
            'modules', 'visualization', 'static', 'multivariate.html')
        )

    @cherrypy.expose
    def cross_lingual(self):
        """Cross Lingual recommender html returned."""
        return file(os.path.join(
            'modules', 'visualization', 'static', 'cross_lingual.html')
        )

    @cherrypy.expose
    def lingual_semantics(self):
        """Semantically related words in same language returned."""
        return file(os.path.join(
            'modules', 'visualization', 'static', 'intra_language.html')
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
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

        trword = word
        if word in self.cached_dictionary:
            return json.dumps(self.cached_dictionary[word])
        else:
            if(language == 'hindi'):
                trword = yandex.get_translation(word, "hi-en")

            dictionary = PyDictionary(trword)
            meanings = []
            meanings.append(trword)
            meanings.append(dictionary.meaning(trword))
            try:
                meanings.append(dictionary.meaning(trword))
            except:
                meanings.append(None)
            if meanings[1]:
                self.cached_dictionary[word] = meanings
                with codecs.open(
                    'cached_dictionary', 'w', encoding='utf-8'
                ) as f:
                    f.write(json.dumps(self.cached_dictionary))
            return json.dumps(meanings)

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
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        model = self.model.get(language)
        if model is not None:
            data = self._recommend(
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
            * :mod:`modules.vector_space_mapper.vector_space_mapper`
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        vm = self.cross_lang_vm.get((lang1, lang2))
        data = None
        if vm is not None:
            data = self._recommend(
                word, int(topn), fn=vm.get_recommendations_from_word
            )
        return data

    @cherrypy.expose
    def _create_vector_space_mapper(self, lang1, lang2):
        """
        Create Vector Space Mapper between Languages.

        API Documentation
            :param language1: Language 1 used for
                building :class:`modules.vector_space_mapper.vector_space_mapper.VectorSpaceMapper` object
            :param language2: Language 2 used for
                building :class:`modules.vector_space_mapper.vector_space_mapper.VectorSpaceMapper` object
            :return: JSON with successful/failure message
            :rtype: JSON

        .. seealso::
            :mod:`modules.vector_space_mapper.vector_space_mapper`
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

    def _recommend(self, word, limit, fn):
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

    def _load_model(self, language):
        """Used to load Word2Vec Model."""
        return Word2Vec.load(
            os.path.join('data', 'models', 't-vex-%s-model' % language)
        )


if __name__ == '__main__':
    """Setting up the Server with Specified Configuration"""

    server_config = ConfigParser.RawConfigParser()
    env = Environment(loader=FileSystemLoader('static'))
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'modules', 'visualization', 'static', 'js'
            )
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'modules', 'visualization', 'static', 'css'
            )
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'modules', 'visualization', 'static', 'images'
            )
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'modules', 'visualization', 'static', 'resources'
            )
        }
    }
    server_config.read(os.path.join('modules', 'visualization', 'server.conf'))
    server_port = server_config.get('Server', 'port')
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
