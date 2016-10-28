#!/usr/bin/env python3

import unittest
import n_gram


class TestNGram(unittest.TestCase):
    def setUp(self):
        self.s1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.s2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"

    def test_unigram(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.s1)
        expected = {"<s>": 1, "HELLO": 1, "MY": 1, "DEAR": 1, "FRIEND": 1, "</s>": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.flush()
        unigram.add_corpus(self.s2)
        expected = {"<s>": 2, "HELLO": 1, "MY": 2, "DEAR": 1, "FRIEND": 2, "</s>": 2, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.add_corpus(self.s1)
        expected = {"<s>": 3, "HELLO": 2, "MY": 3, "DEAR": 2, "FRIEND": 3, "</s>": 3, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

    def test_bigram(self):
        bigram = n_gram.Bigram()
        bigram.add_corpus(self.s1)
        expected = {"<s> HELLO": 1, "HELLO MY": 1, "MY DEAR": 1, "DEAR FRIEND": 1, "FRIEND </s>": 1}
        actual = bigram.get_counts()
        self.assertEqual(expected, actual)
