#! /usr/bin/env python2
"""CherryPy Server to provide recommendations of semantic similarity."""

import cherrypy
import codecs
import os
import ConfigParser
import json
import cPickle
from gensim.models import Word2Vec
from jinja2 import Environment, FileSystemLoader
from modules.vector_space_mapper.vector_space_mapper import VectorSpaceMapper


class Server():
    """Server Configuration for t-vex."""

    def __init__(self):
        """Initialization the Language and Model."""
        self.language = None
        self.cross_lang1 = None
        self.cross_lang2 = None
        self.vm = None
        self.model = None

    @cherrypy.expose
    def index(self):
        """Semantic spac visualization html returned."""
        return file(os.path.join('visualization', 'static', 'index.html'))

    @cherrypy.expose
    def multivariate_analysis(self):
        """Parallel Coordinates for multivariate analysis html page return."""
        return file(os.path.join(
            'visualization', 'static', 'multivariate.html')
        )

    @cherrypy.expose
    def cross_lingual(self):
        """Cross Lingual recommender html returned."""
        return file(os.path.join(
            'visualization', 'static', 'cross_lingual.html')
        )

    @cherrypy.expose
    def retrieve_recommendations(self, language, word, limit=10):
        """
        Retrieve number of semantically similar recommendations.

        For specified word in the given language retrieve limit recommendations
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if self.language is None or self.language != language:
            try:
                self.model = Word2Vec.load(
                    os.path.join(
                        'data', 'models', 't-vex-%s-model' % (language)
                    )
                )
                self.language = language
                data = self._recommend(
                    word, int(limit), fn=self.model.most_similar
                )
            except (IOError, OSError):
                data = json.dumps(None)
        else:
            data = self._recommend(
                word, int(limit), fn=self.model.most_similar
            )
        return data

    @cherrypy.expose
    def get_cross_lingual_recommendations(
        self,
        lang1,
        lang2,
        word,
        topn=10
    ):
        """Provide cross lingual recommendations."""
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if self.cross_lang1 is not lang1 and self.cross_lang2 is not lang2:
            try:
                f = open(os.path.join(
                    'visualization', 'vector_space_mapper', '%s_%s' % (
                        lang1, lang2
                    )
                ), "r")
                self.vm = cPickle.load(f)
                self.cross_lang1 = lang1
                self.cross_lang2 = lang2
                data = self._recommend(
                    word, int(topn), fn=self.vm.get_recommendations_from_word
                )
            except (IOError, OSError):
                data = json.dumps(None)
        else:
            data = self._recommend(
                word, int(topn), fn=self.vm.get_recommendations_from_word
            )
        return data

    @cherrypy.expose
    def create_vector_space_mapper(self, lang1, lang2):
        """Create Vector Space Mapper between Languages."""
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        dir_path = os.path.join(
            'visualization', 'vector_space_mapper'
        )
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if os.path.exists(os.path.join(
            dir_path, '%s_%s' % (lang1, lang2)
        )) is False:
            try:
                model_1 = Word2Vec.load(
                    os.path.join('data', 'models', 't-vex-%s-model' % lang1)
                )
                model_2 = Word2Vec.load(
                    os.path.join('data', 'models', 't-vex-%s-model' % lang2)
                )
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
                    vm = VectorSpaceMapper(model_1, model_2, bilingual_dict)
                    vm.map_vector_spaces()
                    with open(os.path.join(
                        'visualization', 'vector_space_mapper', '%s_%s' % (
                            lang1, lang2
                        )
                    ), "w") as file:
                        cPickle.dump(vm, file)
                        return json.dumps({'msg': 'Success'})
            except (IOError, OSError):
                return json.dumps({'msg': 'Failure'})
        else:
            return json.dumps({'msg': 'Success'})

    def _recommend(self, word, limit, fn):
        """Vector Space Mapper recommend functionality."""
        try:
            vec_list = fn(word, topn=limit)
            data = json.dumps([
                {
                    'word': tup[0],
                    'weight': tup[1]
                } for tup in vec_list
            ])
        except KeyError:
            data = json.dumps(None)
        return data


if __name__ == '__main__':
    ''' Setting up the Server with Specified Configuration'''

    server_config = ConfigParser.RawConfigParser()
    env = Environment(loader=FileSystemLoader('static'))
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'visualization', 'static', 'js'
            )
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'visualization', 'static', 'css'
            )
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'visualization', 'static', 'images'
            )
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                'visualization', 'static', 'resources'
            )
        }
    }
    server_config.read(os.path.join('visualization', 'server.conf'))
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
