import logging
import pathlib

import jinja2

import aiohttp_jinja2
from aiohttp import web
from views import index, get_file, upload_file, get_file_page, antihack, robots

from argument_parser import get_arguments
from settings import config


async def init_app():
    app = web.Application()

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('main', 'templates'))

    app.router.add_get('/', index)
    app.router.add_get('/file/{id}', get_file)
    app.router.add_get('/file/{id}/p', get_file_page)
    app.router.add_post('/upload', upload_file)
    app.router.add_get('/phpmyadmin', antihack)
    app.router.add_get('/phpmyadmin/index.php', antihack)
    app.router.add_get('/robots.txt', robots)

    return app


def main(configuration):
    logging.basicConfig(level=logging.INFO)
    pathlib.Path(configuration.storage_path).mkdir(parents=True, exist_ok=True)

    app = init_app()
    web.run_app(app, port=configuration.port)


if __name__ == '__main__':
    arguments = get_arguments()
    config.hostname = arguments.hostname
    config.port = arguments.port
    config.storage_path = arguments.storage
    print(config)
    main(config)
