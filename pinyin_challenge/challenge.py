import csv
import random
from importlib import resources
from pinyin_challenge.prefix_tree import PrefixTree
from pinyin_challenge.cedict.cedict import cedict_entries




class PinyinChallenge:
    """ Can you give the pinyin given the Chinese character? """

    def __init__(self, filepath):
        selection = self.read_challenge(filepath)
        matching_characters = self.characters_matching_pinyins(selection)
        self.prefix_tree = PrefixTree()
        self.characters = {}
        self.meanings = {}
        for key in selection:
            if key not in matching_characters:
                continue
            char = matching_characters[key]
            self.characters[char.traditional] = char
            self.meanings[char.traditional] = key[1]
            if char.traditional != char.simplified:
                self.characters[char.simplified] = char
                self.meanings[char.simplified] = key[1]
            self.prefix_tree.add(key, char)

    def sample(self):
        characters = list(self.characters)
        return ''.join(random.sample(characters, k=len(characters)))

    @staticmethod
    def characters_matching_pinyins(selection):
        """ Return CE-DICT characters whose pinyin is in selection """
        pinyins = {pinyin for pinyin, _ in selection}
        matching = {}
        not_unique = set()
        for entry in cedict_entries():
            if entry.pinyin not in pinyins:
                continue
            for sense in entry.senses:
                key = (entry.pinyin, sense)
                if key in matching:
                    not_unique.add(key)
                matching[key] = entry
        if not_unique:
            print(f"{not_unique} - not unique")
            matching = {k: v for k, v in matching.items() if k not in not_unique}
        return matching


    @staticmethod
    def read_challenge(filepath):
        selection = []
        with open(filepath) as fileobj:
            for row in csv.DictReader(fileobj, dialect=csv.excel_tab):
                selection.append((row["pinyin"], row["definition"]))
        return selection
