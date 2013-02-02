"""
Test search operations
"""
import shlex

from twisted.trial import unittest

from qontour import search

class SearchTest(unittest.TestCase):
    """
    Verify search results accurately represent what's in the filesystem
    """
    # def setUp(self):

    def test_capsplit(self):
        """
        Split filenames correctly by word
        """
        strings = """
        fooBarMansion-1.html      foo Bar Mansion 1 html
        a_b-1.html                a b 1 html
        a__b-1.html               a b 1 html
        AB-1.html                 AB 1 html
        ab1.html                  ab 1 html
        HTMLDocument.html         HTML Document html
        "foo bar.html"            foo bar html
        ACoolDocument.html        A Cool Document html
        AC8_Dragon_5Headed_AA_DS.png   AC 8 Dragon 5 Headed AA DS png
        """

        for s in strings.splitlines():
            s = s.strip()
            if not s:
                continue
            parts = shlex.split(s)
            inp = parts[0]
            expected = ' '.join(parts[1:])
            actual = search.capsplit(inp)
            self.assertEqual(actual, expected)


