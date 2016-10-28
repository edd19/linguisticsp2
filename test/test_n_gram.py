#!/usr/bin/env python3

import unittest
import n_gram


class TestNGram(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"

    def test_unigram(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.corpus1)
        expected = {"<s>": 1, "HELLO": 1, "MY": 1, "DEAR": 1, "FRIEND": 1, "</s>": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.flush()
        unigram.add_corpus(self.corpus2)
        expected = {"<s>": 2, "HELLO": 1, "MY": 2, "DEAR": 1, "FRIEND": 2, "</s>": 2, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.add_corpus(self.corpus1)
        expected = {"<s>": 3, "HELLO": 2, "MY": 3, "DEAR": 2, "FRIEND": 3, "</s>": 3, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

    def test_bigram(self):
        bigram = n_gram.Bigram()
        bigram.add_corpus(self.corpus1)
        expected = {"<s> HELLO": 1, "HELLO MY": 1, "MY DEAR": 1, "DEAR FRIEND": 1, "FRIEND </s>": 1}
        actual = bigram.get_counts()
        self.assertEqual(expected, actual)

    def test_split_corpus_lines(self):
        ngram = n_gram.NGram()

        expected = ["<s> HELLO MY DEAR FRIEND </s>"]
        actual = list(ngram.split_corpus_sentences(self.corpus1))

        self.assertEqual(expected, actual, "Split corpus should return one sentence")

        expected = ["<s> HELLO MY DEAR FRIEND </s>", "<s> HOW ARE YOU MY FRIEND </s>"]
        actual = list(ngram.split_corpus_sentences(self.corpus2))

        self.assertEqual(expected, actual, "Split corpus should return two sentences")

    def test_split_sentence_n_grams(self):
        ngram = n_gram.NGram()

        expected = ["<s>",  "HELLO", "MY",  "DEAR",  "FRIEND",  "</s>"]
        actual = list(ngram.split_sentence_n_grams(self.corpus1, 1))

        self.assertEqual(expected, actual, "Split sentence should return list of one words")

        expected = ["<s> HELLO", "HELLO MY", "MY DEAR", "DEAR FRIEND", "FRIEND </s>"]
        actual = list(ngram.split_sentence_n_grams(self.corpus1, 2))

        self.assertEqual(expected, actual, "Split sentence should return list of two words")
