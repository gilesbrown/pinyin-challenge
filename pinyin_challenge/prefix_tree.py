""" A simple prefix tree """


from pinyin_challenge.cedict.cedict import CEDictCharacter, strip_accents


class PrefixTree:

    def __init__(self):
        self.tree = {}
        self.char = None
        self.text = None

    def add(self, key, char):
        node = self
        text = f"{key[0]} /{key[1]}/"
        for ch in text:
            if ch not in node.tree:
                node.tree[ch] = PrefixTree()
            node = node.tree[ch]
        assert node.char is None
        node.char = char
        node.text = text

    def search(self, pinyin, i=0):
        # print(f"SEARCH? {pinyin}[{i}] = {pinyin[i:]} {self.char} {self}")
        if self.char is not None:
            yield (self.char, self.text)
        if i >= len(pinyin):
            for node in self.tree.values():
                yield from node.search(pinyin, i + 1)
            return
        if pinyin[i] in self.tree:
            yield from self.tree[pinyin[i]].search(pinyin, i + 1)
