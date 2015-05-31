# -*- coding: utf-8 -*-
import uuid

# import Tornado
import tornado.ioloop
import tornado.web
from tornado.options import options, define

# import SockJS
import sockjs.tornado

from gorinich.handlers import SyncConnection, PadHandler, IndexHandler
from gorinich.core import Application
from utils import TEMPLATES_ROOT, STATIC_ROOT

__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '24.05.2015'

define("port", default=8080, help="app port", type=int)
define("pad_lifetime", default=10, help="pad lifetime (minutes)", type=int)
define("cookie_secret", default=uuid.uuid4().hex, help="cookie secret", type=str)


def run_app():
    options.parse_command_line()

    # 1. Create sync router
    sync_router = sockjs.tornado.SockJSRouter(SyncConnection, '/sync')

    # 2. Create Tornado application
    app = Application(
        [
            (r'/', IndexHandler),
            (r'/(?P<pad_id>[0-9a-z\-]+)', PadHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_ROOT})
        ] + sync_router.urls,
        cookie_secret=options.cookie_secret,
        static_url_prefix='/static/',
        template_path=TEMPLATES_ROOT,
        pad_lifetime=options.pad_lifetime,
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(options.port)
    logging.info("App started, visit http://localhost:%s" % options.port)
    logging.info("App started with options: %r" % options.as_dict())

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()


def main():
    try:
        run_app()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.DEBUG)

    main()
