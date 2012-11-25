"""
Qontour resources
"""

import json
import os.path
from cStringIO import StringIO

import yaml

from twisted.web.static import File, Data

from klein import resource, route

from qontour import search, IMAGE_ROOT


@route('/i/')
def images(request):
    return File(IMAGE_ROOT.path)

@route('/static/')
def static(request):
    return File('./static')

@route('/ilist')
def imageList(request):
    query = request.args.get('q', ['banana'])[0]
    ss = search.Search(query)
    return json.dumps(ss.results())

@route('/')
def index(request):
    with open('./static/index.html') as f:
        return f.read()

