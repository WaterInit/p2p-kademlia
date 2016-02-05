from django.http import HttpResponse
from .lib import gpg, database


def add(request):

    dict = request.POST
    key_ascii = dict['keytext']

    code = database.insert_key(key_ascii)

    response = HttpResponse()

    if code != 0:
        response.status_code = 500

    return response


def lookup(request):

    parameters = request.GET
    operation = parameters['op']
    search_string = parameters['search']

    response = HttpResponse()

    if operation == 'get':
        # GET KEY

        key_id = search_string.split('x')[1]
        key_id = key_id[-8:]
        key = database.get_key(key_id)

        if key is not None:
            response['content_type'] = 'application/pgp-keys; charset=UTF-8'
            response.content = key

        else:

            response.status_code = 404

    elif operation == 'index':
        # SEARCH FOR KEY

        key_id = search_string
        info = database.get_metadata(key_id)

        if info is not None:
            content_string = "info:1:1\n" + \
                             "pub:" + info['fingerprint'] + ":" + info['algo']  + ":" + str(info['length']) + ":" + info['date'] + ":" + info['expires'] + ":\n" + \
                             "uid:" + info['uids'][0] + ":" + info['date'] + "::\n"

            response.content = content_string

    return response
