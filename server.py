#! /usr/bin/env python3
import cherrypy
import os
import ConfigParser
import json
from gensim.models import Word2Vec
from jinja2 import Environment, FileSystemLoader


class Server():
    '''
        Server Configuration:
    '''


    def __init__(self):
        """ Initialization the URL of the comic and transcript """

        self.language = None
        self.model = None

    @cherrypy.expose
    def retrieve_recommendations(self, language, word, limit=10):
        """ Render the index page """

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if self.language is None or self.language != language:
            try:
                self.model = Word2Vec.load('./models/t-vex-%s-model' %(language))
                self.language = language
                data = self._recommend(word, int(limit))
            except IOError:
                data = json.dumps(None)
        else:
            data = self._recommend(word, int(limit))
        return data

    def _recommend(self, word, limit):
        try:
            vec_list = self.model.most_similar(word, topn=limit)
            data = json.dumps([
                {
                    'word': tup[0],
                    'weight': tup[1]
                } for tup in vec_list
            ])
        except KeyError:
            data = json.dumps([])
        return data

if __name__ == '__main__':
    ''' Setting up the Server with Specified Configuration'''

    server_config = ConfigParser.RawConfigParser()
    env = Environment(loader=FileSystemLoader(''))
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
    }
    server_config.read('server.conf')
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
