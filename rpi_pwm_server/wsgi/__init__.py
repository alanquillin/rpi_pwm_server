from flask import Flask
from flask_restful import Api
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from rpi_pwm_server.wsgi import pwm

import logging

LOG = logging.getLogger(__name__)


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


api.add_resource(pwm.PWMResourse, '/')


def run():
    LOG.info('Starting web server...')
    LOG.debug('Enable port: %s', 8081)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8081)
    IOLoop.instance().start()


def stop():
    LOG.info('Stopping web server...')
    IOLoop.instance().stop()
