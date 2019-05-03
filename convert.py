from collections import defaultdict
from json import dump
from nltk.corpus import words as english


class WordDict:
    tree = {}

    def __init__(self, path_out: str):
        for word in english.words():
            self.add(word.strip().lower())

        with open(path_out, 'w') as o:
            dump(self.tree, o)

    def add(self, word: str):
        cur = self.tree
        for l in word:
            if l not in cur:
                cur[l] = {}

            cur = cur[l]

        cur["word"] = True


WordDict('public/dict.json')
