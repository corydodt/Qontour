"""
Search interface for image files
"""

import re
from pipes import quote
from subprocess import check_output, CalledProcessError
import urllib

from qontour import IMAGE_ROOT

def locate(s):
    """
    locate any paths under IMAGE_ROOT that match the query string <s>
      => [FilePaths]
    """
    irp = IMAGE_ROOT.path
    cmd = ["locate", "-ir"] + ['^' + irp + "/.*" + quote(s)]
    try:
        found = check_output(cmd).strip().replace('\r', '').split('\n') 
        return [IMAGE_ROOT.preauthChild(f) for f in found]
    except CalledProcessError, e:
        print e
        return []

class Search(object):
    """
    A search operation
    """
    def __init__(self, query):
        self.query = query

    def _urls(self, *paths):
        ret = []
        lirp = len(IMAGE_ROOT.path)
        for p in paths:
            ret.append(urllib.quote('/i' + p.path[lirp:], '/'))
        return ret

    def results(self):
        res = locate(self.query)
        urls = self._urls(*res)
        return urls

