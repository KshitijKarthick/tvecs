#! /usr/bin/env python2
"""CherryPy Server to provide recommendations of semantic similarity."""

import cherrypy
import os
import ConfigParser
import json
import cPickle
from gensim.models import Word2Vec
from jinja2 import Environment, FileSystemLoader


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
        """Index page returns static index.html."""
        
        return file(os.path.join('visualization','static', 'index.html'))

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
                data = self._recommend(word, int(limit), fn=self.model.most_similar)
            except IOError:
                data = json.dumps(None)
        else:
            data = self._recommend(word, int(limit), fn=self.model.most_similar)
        return data

    @cherrypy.expose
    def get_cross_lingual_recommendations(self, lang1, lang2, word, topn=10):

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if self.cross_lang1 is not lang1 and self.cross_lang2 is not lang2:
            try:
                f = open('%s_%s' %(lang1, lang2), "r")
                self.vm = cPickle.load(f)
                self.cross_lang1 = lang1
                self.cross_lang2 = lang2
                data = self._recommend(word, int(topn), fn=self.vm.get_recommendations_from_word)
            except IOError:
                data = json.dumps(None)
        else:
            data = self._recommend(word, int(topn), fn=self.vm.get_recommendations_from_word)
        return data


    def _recommend(self, word, limit, fn):
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
            'tools.staticdir.dir': os.path.join('visualization', 'static', 'js')
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join('visualization', 'static', 'css')
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join('visualization', 'static', 'images')
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
