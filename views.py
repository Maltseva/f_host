import logging
import os
import uuid

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from settings import HOSTNAME, FORBIDDEN_FILE_NAMES, STORAGE_PATH

log = logging.getLogger(__name__)


async def upload_file(request):
    reader = await request.multipart()
    file = await reader.next()
    original_filename = replace_forbidden_file_name(file.filename)
    log.info(f"Uploading file...: {original_filename}")
    newdir = f'{str(uuid.uuid4())}'
    os.mkdir(f"{STORAGE_PATH}/{newdir}/")
    size = 0
    link = f'{HOSTNAME}/file/{newdir}/p'
    with open(os.path.join(STORAGE_PATH, newdir, original_filename), 'wb') as f:
        while True:
            chunk = await file.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    log.info(f"Uploaded file: {original_filename}, Size:{size} bytes")
    return web.json_response({
        "uploaded_file": {"file_link": link, "file_name": original_filename, "file_id": newdir, "file_size": sizeof_fmt(size)}
    })


async def index(request):
    return aiohttp_jinja2.render_template(
        'index.html',
        request,
        {"request": {"url": f"{HOSTNAME}/upload"}}
    )


async def get_file(request):
    file_id = request.match_info.get('id')
    try:
        files = os.listdir(f'{STORAGE_PATH}/{file_id}/')
        if files:
            return web.FileResponse(
                f'{STORAGE_PATH}/{file_id}/{files[0]}',
                headers={'Content-Disposition': f'Attachment;filename={files[0]}'}
            )
        else:
            return web.HTTPNotFound()
    except FileNotFoundError:
        return web.HTTPNotFound()


async def get_file_page(request):
    file_id = request.match_info.get('id')
    try:
        files = os.listdir(f'{STORAGE_PATH}/{file_id}/')
        if files:
            filename = files[0]
            filesize = sizeof_fmt(os.path.getsize(f'{STORAGE_PATH}/{file_id}/{filename}'))
            link = f'{HOSTNAME}/file/{file_id}'
            return aiohttp_jinja2.render_template(
                'file.html',
                request,
                {"file": {"url": link, "filename": filename, "size": filesize}, "data": {"hostname": HOSTNAME}}
            )
        else:
            return web.HTTPNotFound()
    except FileNotFoundError:
        return web.HTTPNotFound()


def replace_forbidden_file_name(filename):
    filename_without_ext = filename.split('.')[0]
    if filename_without_ext.upper() in FORBIDDEN_FILE_NAMES:
        log.info(f"Replacing filename {filename}")
        return f'file-{filename}'
    else:
        return filename


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)