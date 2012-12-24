"""
Search interface for image files
"""

import os
import re
import string
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
        hits = locate(self.query)
        ret = []
        for hit, url in zip(hits, self._urls(*hits)):
            label = capsplit(
                    ''.join(os.path.splitext(
                        hit.basename()
                        )[:-1]))
            ret.append({
                'label': label,
                'url': url,
                })
        return ret


RX = re.compile(r'[^a-zA-Z0-9]')

def capsplit(s):
    """
    Split s by punctuation and capitalization, attempting to preserve acronyms
    """
    s = re.sub(r'([A-Z])', r' \1', s).strip()
    items = RX.split(s)

    buf = []
    x = []
    for item in items:
        if len(item) == 1 and item in string.uppercase:
            buf.append(item)
        else:
            if buf:
                x.extend([''.join(buf), item])
            else:
                x.append(item)
            buf = []
    return ' '.join(x)
