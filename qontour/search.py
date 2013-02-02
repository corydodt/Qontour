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


def capsplit(s):
    """
    Split s by punctuation and capitalization, attempting to preserve acronyms

    - split into runs of capital letters, lowercase letters, and other
      characters

    - runs of lowercase letters are considered single words. if preceded by a
      capital letter, that letter is part of the word

    - after removing initial capitals for lowercase words, all continuous runs
      of capital letters are acronyms and kept together.

    - discard all punctuation
    """
    uc = string.uppercase
    lc = string.lowercase
    digits = string.digits
    other = object()

    def category(c):
        if c is None:
            return None
        if c in lc:
            return lc
        if c in uc:
            return uc
        if c in digits:
            return digits
        return other

    runs = []
    def finish(run):
        run[1] = ''.join(run[1])
        runs.append(run)

    ss = list(s)
    run = None
    for cur, prev in zip(ss, [None]+ss):
        cat = category(cur)
        if cat != category(prev):
            # new character class
            if run is not None:
                finish(run)
            run = [cat, [cur]]
        else:
            run[1].append(cur)
    finish(run)

    for n, (ccur, cprev) in enumerate(zip(runs, [None]+runs)):
        if ccur[0] == lc:
            # lowercase, preceded by uppercase:
            # grab one character from the end of the uc group and insert it
            # into the lowercase group
            if cprev and cprev[0] == uc:
                _lastChar = cprev[1][-1]
                cprev[1] = cprev[1][:-1]
                ccur[1] = _lastChar + ccur[1]


    runs = [r for r in runs if r[0] is not other and r[1]]
    return ' '.join(zip(*runs)[1])

