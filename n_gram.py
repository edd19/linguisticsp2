#!/usr/bin/env python3


class NGram(object):
    def __init__(self, n=1):
        self.counts = {}
        self.n = n
        self.word_occurences = 0

    def add_corpus(self, corpus):
        for n_gram in self.get_n_grams(corpus):
            self.update_counts(n_gram)

    def update_counts(self, n_gram):
        if n_gram in self.counts:
            self.counts[n_gram] += 1
        else:
            self.counts[n_gram] = 1

    def get_counts(self):
        return self.counts

    def get_size(self):
        return len(self.counts)

    def get_n_gram_count(self, n_gram):
        frequency = self.counts.get(n_gram, None)
        if frequency:
            return frequency
        frequency = self.counts.get("<UNK>", 0)
        return frequency

    def get_top_n_by_counts(self, n):
        n_gram_with_counts = list(self.counts.items())
        n_gram_with_counts.sort(key=lambda x: x[1], reverse=True)
        return n_gram_with_counts[0:n]

    def flush(self):
        self.counts = {}
        self.word_occurences = 0

    @staticmethod
    def split_corpus_sentences(corpus):
        corpus_left = corpus
        separator = "</s>"  # Signify end of sentence
        while len(corpus_left) > 0:
            sentence, sep, corpus_left = corpus_left.partition(separator)
            sentence += separator
            yield sentence.strip()

    def split_sentence_n_grams(self, sentence, n):
        words = sentence.split()
        self.word_occurences += len(words)
        n_gram = []
        for word in words:
            n_gram.append(word)
            if len(n_gram) >= n:
                yield " ".join(n_gram)
                n_gram.pop(0)

    def get_n_grams(self, corpus):
        for sentence in self.split_corpus_sentences(corpus):
            for n_gram in self.split_sentence_n_grams(sentence, self.n):
                yield n_gram

    def discard_unfrequent_n_grams(self, min_counts):
        n_gram_with_counts = list(self.counts.items())
        self.counts["<UNK>"] = 0  # Replace discarded elements by the unknown tag
        discarded_n_grams = []
        for (n_gram, count) in n_gram_with_counts:
            if count <= min_counts:
                self.counts["<UNK>"] += count
                del self.counts[n_gram]
                discarded_n_grams.append(n_gram)
        return discarded_n_grams

    def get_word_occurences(self):
        return self.word_occurences

class Unigram(NGram):
    def __init__(self):
        super(self.__class__, self).__init__(n=1)


class Bigram(NGram):
    def __init__(self):
        super(self.__class__, self).__init__(n=2)


class Trigram(NGram):
    def __init__(self):
        super(self.__class__, self).__init__(n=3)


