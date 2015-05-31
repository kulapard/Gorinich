# -*- coding: utf-8 -*-
from objects import PadStorage

__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '24.05.2015'

import uuid
from datetime import datetime, timedelta

import tornado.web
import tornado.ioloop

from gorinich import logger
from gorinich.utils import get_server_address


class Application(tornado.web.Application):
    # How often this application will clean old sessions (tokens)
    CLEAN_SESSION_INTERVAL = 60 * 60  # in seconds
    OLD_SESSION_LIFETIME = 60 * 60  # in seconds

    CLEAN_PADS_INTERVAL = 60 * 60  # in seconds

    # How often this application will send Ping
    PING_INTERVAL = 60  # in seconds

    def __init__(self, *args, **kwargs):
        # initialize tornado's application
        super(Application, self).__init__(*args, **kwargs)

        # create unique uid for this application
        self.uid = uuid.uuid4().hex

        # initialize dict to keep administrator's connections
        self.admin_connections = {}

        # dictionary to keep client's connections
        self.connections = {}

        # application engine
        self.engine = None

        self.address = get_server_address()

        self.pad_storage = PadStorage(pad_lifetime=self.settings['pad_lifetime'])


    def initialize(self):
        self.init_engine()
        # self.init_ping()
        # self.init_clean_sessions()
        self.init_clean_pads()

    def init_engine(self):
        """
            Initialize engine.
        """
        tornado.ioloop.IOLoop.instance().add_callback(self.engine.initialize)

    def init_ping(self):
        """
            Start periodic tasks for sending quotes to all clients.
        """
        self.send_ping_periodically = tornado.ioloop.PeriodicCallback(
            callback=self.send_ping,
            callback_time=self.PING_INTERVAL * 1000
        )
        self.send_ping_periodically.start()
        logger.info('Ping initialized')

    def update_ping_interval(self, ping_interval):
        """
            Update quote interval.
        """
        self.send_ping_periodically.stop()
        self.send_ping_periodically = tornado.ioloop.PeriodicCallback(
            callback=self.send_ping,
            callback_time=ping_interval * 1000
        )
        self.send_ping_periodically.start()

    def send_ping(self):
        """
            Send Ping! to all clients
        """
        self.engine.publish_public_message('Ping!')

    # def init_clean_sessions(self):
    #     """
    #     Start periodic tasks for cleaning old activated sessions.
    #     """
    #     tornado.ioloop.PeriodicCallback(
    #         callback=self.clean_sessions,
    #         callback_time=self.CLEAN_SESSION_INTERVAL * 1000
    #     ).start()
    #     logger.info('Clean session initialized')

    # def clean_sessions(self):
    #     """
    #         Remove old activated sessions
    #     """
    #     logger.info('Starting clean sessions')
    #     active_account_ids = self.engine.get_account_ids()
    #     create_date_before = datetime.utcnow() - timedelta(seconds=self.OLD_SESSION_LIFETIME)
    #     session_manager.remove_activated(
    #         exclude_account_ids=active_account_ids,
    #         create_date_before=create_date_before
    #     )

    def init_clean_pads(self):
        """
        Start periodic tasks for cleaning old pads sessions.
        """
        tornado.ioloop.PeriodicCallback(
            callback=self.clean_pads,
            callback_time=self.CLEAN_PADS_INTERVAL * 1000
        ).start()
        logger.info('Clean pads initialized')

    def clean_pads(self):
        logger.info('Starting clean pads')
        self.pad_storage.delete_expired_pads()

        # def add_connection(self, account_id, uid, client):
        #     """
        #     Register new client's connection.
        #     """
        #     if account_id not in self.connections:
        #         self.connections[account_id] = {}
        #
        #     self.connections[account_id][uid] = client
        #
        # def remove_connection(self, account_id, uid):
        #     """
        #     Remove client's connection
        #     """
        #     try:
        #         del self.connections[account_id][uid]
        #     except KeyError:
        #         pass
        #
        #     # Clean only empty connections list
        #     if account_id in self.connections and not self.connections[account_id]:
        #         try:
        #             del self.connections[account_id]
        #         except KeyError:
        #             pass
        #
        # def add_admin_connection(self, uid, client):
        #     """
        #     Register administrator's connection (from web-interface).
        #     """
        #     self.admin_connections[uid] = client
        #
        # def remove_admin_connection(self, uid):
        #     """
        #     Remove administrator's connection.
        #     """
        #     try:
        #         del self.admin_connections[uid]
        #     except KeyError:
        #         pass
