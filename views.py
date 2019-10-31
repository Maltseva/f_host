import logging
import os
import uuid

import aiohttp
import aiohttp_jinja2
from aiohttp import web

HOSTNAME = 'http://k4m454k.hldns.ru:19100'
# HOSTNAME = 'http://localhost:8090'


log = logging.getLogger(__name__)


async def upload_file(request):
    reader = await request.multipart()
    file = await reader.next()
    original_filename = file.filename
    log.info(f"Uploading file...: {original_filename}")
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
    log.info(f"Uploaded file: {original_filename}, Size:{size} bytes")
    return web.json_response({"message": f"{HOSTNAME}/file/{newdir}"})


async def index(request):
    return aiohttp_jinja2.render_template('index2.html', request, {"request": {"url": f"{HOSTNAME}/upload"}})


async def get_file(request):
    file_id = request.match_info.get('id')
    try:
        files = os.listdir(f'files/{file_id}/')
        if files:
            return web.FileResponse(f'files/{file_id}/{files[0]}', headers={'Content-Disposition': f'Attachment;filename={files[0]}'})
        else:
            return web.HTTPNotFound()
    except FileNotFoundError:
        return web.HTTPNotFound()


