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
