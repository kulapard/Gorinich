# -*- coding: utf-8 -*-
import uuid

import tornado.web
import sockjs.tornado

from gorinich.base import BaseHandler

__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '24.05.2015'


class IndexHandler(BaseHandler):
    """Regular HTTP handler to serve the index page"""

    def get(self):
        self.set_secure_cookie('uid', uuid.uuid4().hex)
        pad = self.application.pad_storage.crate_pad()
        self.redirect('/%s' % pad.pad_id)


class PadHandler(BaseHandler):
    """Regular HTTP handler to serve the pad page"""

    def get(self, pad_id):
        if pad_id not in self.application.pad_storage:
            raise tornado.web.HTTPError(404)

        pad = self.application.pad_storage.get_pad(pad_id)
        uid = self.get_secure_cookie('uid')
        self.render_template('pad.jinja2', pad=pad, uid=uid)


class SyncConnection(sockjs.tornado.SockJSConnection):
    """Sync connection implementation"""
    # Class level variable
    participants_by_pad_id = {}
    pad_id_by_participant = {}

    def on_open(self, request):
        pad_id = request.arguments.get('pad_id')[0]

        if not pad_id:
            raise tornado.web.HTTPError(404)

        if pad_id not in self.participants_by_pad_id:
            self.participants_by_pad_id[pad_id] = set()

        self.pad_id = pad_id
        pad_participants = self.participants_by_pad_id[pad_id]

        # Send that someone joined
        self.broadcast(pad_participants, "Someone joined.")

        # Add client to the clients list
        pad_participants.add(self)

    def on_message(self, message):
        # pad_id = self.pad_id_by_participant[self]
        pad_participants = self.participants_by_pad_id[self.pad_id]

        # Broadcast message
        self.broadcast(pad_participants, message)

    def on_close(self):
        # pad_id = self.pad_id_by_participant[self]
        pad_participants = self.participants_by_pad_id[self.pad_id]

        # Remove client from the clients list and broadcast leave message
        pad_participants.remove(self)

        self.broadcast(pad_participants, "Someone left.")
