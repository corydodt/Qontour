"""
Manage the persistence of thumbnails
"""

from cStringIO import StringIO

from PIL import Image

from pymongo import MongoClient
from bson.binary import Binary

from qontour import IMAGE_ROOT


THUMB_SIZE = 256, 256

_conn = None

def connect(connector=MongoClient):
    global _conn
    _conn = connector()


class ThumbDB(object):
    def __init__(self, connection):
        self.connection = connection
        self.db = connection.thumbs
        self.thumbs = self.db.thumbs

    def __setitem__(self, key, data):
        self.thumbs.insert({'partialURL': key, 'data': data})

    def __getitem__(self, key):
        ret = self.thumbs.find_one({'partialURL': key})
        if not ret:
            self.create(key)
        return ret['data']

    def __contains__(self, key):
        return not not self.thumbs.find({'partialURL': key}).count()

    def create(self, partialURL):
        """
        Read image file at partialURL, store a thumbnail => thumbnail Binary 
        """
        child = IMAGE_ROOT.preauthChild(partialURL[1:])
        if child.is_dir():
            return ''
        im = Image.open(child.path)
        im.thumbnail(THUMB_SIZE)
        io = StringIO()
        im.save(io, child.splitext()[-1][1:])
        ret = self[partialURL] = Binary(io.getvalue())
        return ret

connect()
thumbdb = ThumbDB(_conn)
