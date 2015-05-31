# -*- coding: utf-8 -*-
import logging
import uuid
from datetime import datetime, timedelta

__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '24.05.2015'


class Pad(object):
    def __init__(self, pad_id, lifetime):
        self._pad_id = pad_id
        self.expire_at = datetime.utcnow() + timedelta(minutes=lifetime)
        self._participants = set()

    def __repr__(self):
        return "<%s (pad_id=%s, expire_at=%s)>" % (
            self.__class__.__name__,
            self.pad_id,
            self.expire_at
        )

    @property
    def pad_id(self):
        return self._pad_id

    def add_participant(self, participant):
        self._participants.add(participant)

    def remove_participant(self, participant):
        self._participants.remove(participant)


class PadStorage(object):
    def __init__(self, pad_lifetime):
        self._pad_lifetime = pad_lifetime
        self._pads = {}

    def __contains__(self, item):
        if isinstance(item, Pad):
            return item.pad_id in self._pads

        return item in self._pads

    def get_pad(self, pad_id):
        return self._pads[pad_id]

    def crate_pad(self):
        pad_id = self.generate_pad_id()
        pad = Pad(pad_id=pad_id, lifetime=self._pad_lifetime)
        self._pads[pad_id] = pad
        logging.info('Pad created: %r', pad)
        return pad

    def generate_pad_id(self):
        pad_id = self.generate_random_key()
        while pad_id in self._pads:
            pad_id = self.generate_random_key()

        return pad_id

    @staticmethod
    def generate_random_key():
        return uuid.uuid4().hex

    def delete_expired_pads(self):
        logging.info("Starting pads cleaning...")
        current_time = datetime.utcnow()

        for pad_id in self._pads.keys():
            pad = self._pads[pad_id]
            if pad.expire_at <= current_time:
                self._pads.pop(pad_id)
                logging.info('Pad deleted: %r', pad_id)

        logging.info("Pads cleaning done!")
