#!/usr/bin/env python3


class NGram(object):
    def __init__(self, n=1):
        self.counts = {}
        self.n = n

    def add_corpus(self, corpus):
        for word in corpus.split():
            self.update_counts(word)

    def update_counts(self, word):
        if word in self.counts:
            self.counts[word] += 1
        else:
            self.counts[word] = 1

    def get_counts(self):
        return self.counts

    def flush(self):
        self.counts = {}


class Unigram(NGram):
    def __init__(self):
        super(self.__class__, self).__init__(n=1)



