import logging
import os
import uuid

import aiohttp_jinja2
from aiohttp import web
from settings import config

log = logging.getLogger(__name__)


async def upload_file(request):
    reader = await request.multipart()
    file = await reader.next()

    original_filename = replace_forbidden_file_name(file.filename)
    log.info(f"Uploading file...: {original_filename}")

    file_id = f'{str(uuid.uuid4())}'

    os.mkdir(f"{config.storage_path}/{file_id}/")
    size = 0
    link = f'{config.hostname}/file/{file_id}/p'

    with open(os.path.join(config.storage_path, file_id, original_filename), 'wb') as f:
        while True:
            chunk = await file.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    log.info(f"Uploaded file: {original_filename}, Size:{size} bytes")
    return web.json_response({
        "uploaded_file": {
            "file_link": link,
            "file_name": original_filename,
            "file_id": file_id,
            "file_size": sizeof_fmt(size)
        }
    })


async def index(request):
    return aiohttp_jinja2.render_template(
        'index.html',
        request,
        {"request": {"url": f"{config.hostname}/upload"}}
    )


async def get_file(request):
    """
    This function fuck you!
    :param request:
    :return: web.HTTP object
    """
    file_id = request.match_info.get('id')

    try:
        files = os.listdir(f'{config.storage_path}/{file_id}/')
        if files:
            log.info(f"Download file ID: {file_id}, Name: {files[0]}")
            return web.FileResponse(
                f'{config.storage_path}/{file_id}/{files[0]}',
                headers={'Content-Disposition': f'Attachment;filename={files[0]}'}
            )
        else:
            log.info(f"404 Files not found in ID: {file_id}")
            return web.HTTPNotFound()

    except FileNotFoundError:
        log.info(f"404 for not found ID: {file_id}")
        return web.HTTPNotFound()


async def get_file_page(request):
    file_id = request.match_info.get('id')

    try:
        files = os.listdir(f'{config.storage_path}/{file_id}/')
        if files:
            filename = files[0]
            filesize = sizeof_fmt(os.path.getsize(f'{config.storage_path}/{file_id}/{filename}'))
            link = f'{config.hostname}/file/{file_id}'
            log.info(f"Open download page for ID: {file_id} and {filename}")
            return aiohttp_jinja2.render_template(
                'file.html',
                request,
                {
                    "file": {"url": link, "filename": filename, "size": filesize},
                    "data": {"hostname": config.hostname}
                }
            )
        else:
            log.info(f"404 download page not found files ID: {file_id}")
            return web.HTTPNotFound()

    except FileNotFoundError:
        log.info(f"404 download page bad ID: {file_id}")
        return web.HTTPNotFound()


def replace_forbidden_file_name(filename):
    filename_without_ext = filename.split('.')[0]

    if filename_without_ext.upper() in config.forbidden_filenames:
        log.info(f"Replacing filename {filename}")
        return f'file-{filename}'
    else:
        return filename


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)
