import logging
import os
import uuid

import aiohttp
import aiohttp_jinja2
from aiohttp import web

HOSTNAME = 'http://localhost:8080'

log = logging.getLogger(__name__)


async def upload_file(request):
    reader = await request.multipart()
    file = await reader.next()
    original_filename = file.filename
    newdir = f'{str(uuid.uuid4())}'
    os.mkdir(f"files/{newdir}/")
    size = 0
    link = f'{HOSTNAME}/file/{newdir}'
    with open(os.path.join('files', newdir, original_filename), 'wb') as f:
        while True:
            chunk = await file.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    return aiohttp_jinja2.render_template('file.html', request, {"filename": original_filename, "link": link})


async def index(request):
    return aiohttp_jinja2.render_template('index.html', request, {})


async def get_file(request):
    file_id = request.match_info.get('id')
    try:
        files = os.listdir(f'files/{file_id}/')
        if files:
            return web.FileResponse(f'files/{file_id}/{files[0]}')
        else:
            return web.HTTPNotFound()
    except FileNotFoundError:
        return web.HTTPNotFound()


