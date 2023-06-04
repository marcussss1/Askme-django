#!/usr/bin/env python

def app(env, start_response):

    start_response('200 OK', [('Content-Type','text/html')])
    method = bytes(env['REQUEST_METHOD'], encoding='utf8')
    parameters = {}

    if method == b'GET':
        parameters = bytes(env['QUERY_STRING'], encoding='utf8')

    elif method == b'POST':
        parameters = env['wsgi.input'].read()

    else:
        return [b'Other Method' + b'\n']

    return [method + b'\n' + parameters + b'\n']
