import logging

import jinja2

import aiohttp_jinja2
from aiohttp import web
from views import index, get_file, upload_file, get_file_page


async def init_app():
    app = web.Application()

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('main', 'templates'))

    app.router.add_get('/', index)
    app.router.add_get('/file/{id}', get_file)
    app.router.add_get('/file/{id}/p', get_file_page)
    app.router.add_post('/upload', upload_file)

    return app


def main():
    logging.basicConfig(level=logging.INFO)

    app = init_app()
    web.run_app(app, port=8090)


if __name__ == '__main__':
    main()
