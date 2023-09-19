""" Wraper for https://www.mdbg.net/chinese/dictionary?page=cc-cedict """

import re
import fileinput
import unicodedata as ud
from functools import cached_property
from pinyin_challenge.cedict.download import download_to_tempdir


parse_line = re.compile("""
    (?P<traditional>[^\s]+) \s
    (?P<simplified>[^\s]+) \s
    \[
    (?P<pinyin>[^]]+)
    \]
    \s
    (?P<raw_description>/.*/)
    $
""",
re.VERBOSE
)


def strip_accents(s):
   return ''.join(c for c in ud.normalize('NFD', s) if ud.category(c) != 'Mn')
   # return ud.normalize('NFD', s)


class CEDictCharacter:

    def __init__(self, *, traditional, simplified, pinyin, raw_description):
        self.traditional = traditional
        self.simplified = simplified
        self.pinyin = pinyin
        self.raw_description = raw_description

    @classmethod
    def from_match(cls, match):
        return cls(**match.groupdict())

    @cached_property
    def senses(self):
        return set(self.raw_description.split('/')[1:-1])

    @property
    def description(self):
        return f"{self.pinyin} {self.raw_description}"

    def __repr__(self):
        return f"{self.__class__.__name__}(character='{self.traditional}')"

    def characters(self):    
        return zip(self.description, strip_accents(self.description))



def cedict_entries():
    with open(download_to_tempdir()) as fileobj:
        for line in fileobj:
            if line.startswith('#'):
                continue
            match = parse_line.match(line)
            # exclude composites of characters (having multiple pinyin values)
            if ' ' in match.group('pinyin'):
                continue

            character = CEDictCharacter.from_match(match)
            # print(f"{m.group('p')}|{m.group('t')}|{m.group('m')}")
            # print(f"{m.group('p')}|{m.group('t')}|{m.group('s')}|{m.group('m')}")
            yield character
