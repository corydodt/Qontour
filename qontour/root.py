"""
Qontour resources
"""

import json
from os.path import relpath
import urllib

from twisted.web.static import File, Data

from klein import resource, route
(resource) # for pyflakes

from qontour import search, IMAGE_ROOT
from qontour.thumbs import thumbdb


@route('/i/')
def images(request):
    return File(IMAGE_ROOT.path)

@route('/static/')
def static(request):
    return File('./static')

@route('/thumb/')
def thumb(request):
    """
    Requests to /thumb/xxx/image.jpg will return data from a mongodb
    """
    partialURL = urllib.unquote('/' + relpath(request.path, '/thumb'))
    ret = Data(thumbdb[partialURL], 'image/png')
    ret.isLeaf = True
    return ret

@route('/ilist')
def imageList(request):
    query = request.args.get('q', ['banana'])[0]
    ss = search.Search(query)
    return json.dumps(ss.results())

@route('/')
def index(request):
    """
    Return index.html as a static file - note ./static must contain a file
    named index.html

    Possible klein bug: if File() is an actual path to index.html, instead of
    the containing directory, this doesn't work (404)
    """
    fl = File('./static/index.html')
    fl.isLeaf = True
    return fl

