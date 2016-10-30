#!/usr/bin/env python3

import unittest
import n_gram


class TestNGram(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<S> HELLO MY DEAR FRIEND </S>"
        self.corpus2 = "<S> HELLO MY DEAR FRIEND </S>\n<S> HOW ARE YOU MY FRIEND </S>"
        self.corpus3 = "<S> THIS THIS IS MY MY VICTORY THIS NIGHT </S>"

    def test_unigram(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.corpus1)
        expected = {"<S>": 1, "HELLO": 1, "MY": 1, "DEAR": 1, "FRIEND": 1, "</S>": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.flush()
        unigram.add_corpus(self.corpus2)
        expected = {"<S>": 2, "HELLO": 1, "MY": 2, "DEAR": 1, "FRIEND": 2, "</S>": 2, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

        unigram.add_corpus(self.corpus1)
        expected = {"<S>": 3, "HELLO": 2, "MY": 3, "DEAR": 2, "FRIEND": 3, "</S>": 3, "HOW": 1, "ARE": 1, "YOU": 1}
        actual = unigram.get_counts()
        self.assertEqual(expected, actual)

    def test_bigram(self):
        bigram = n_gram.Bigram()
        bigram.add_corpus(self.corpus1)
        expected = {"<S> HELLO": 1, "HELLO MY": 1, "MY DEAR": 1, "DEAR FRIEND": 1, "FRIEND </S>": 1}
        actual = bigram.get_counts()
        self.assertEqual(expected, actual)

        bigram.flush()
        bigram.add_corpus(self.corpus2)
        expected = {"<S> HELLO": 1, "HELLO MY": 1, "MY DEAR": 1, "DEAR FRIEND": 1, "FRIEND </S>": 2, "<S> HOW": 1,
                    "HOW ARE": 1, "ARE YOU": 1, "YOU MY": 1, "MY FRIEND": 1}
        actual = bigram.get_counts()
        self.assertEqual(expected, actual)

    def test_trigram(self):
        trigram = n_gram.Trigram()
        trigram.add_corpus(self.corpus1)
        expected = {"<S> HELLO MY": 1, "HELLO MY DEAR": 1, "MY DEAR FRIEND": 1, "DEAR FRIEND </S>": 1}
        actual = trigram.get_counts()
        self.assertEqual(expected, actual)

    def test_split_corpus_lines(self):
        ngram = n_gram.NGram()

        expected = ["<S> HELLO MY DEAR FRIEND </S>"]
        actual = list(ngram.split_corpus_sentences(self.corpus1))

        self.assertEqual(expected, actual, "Split corpus should return one sentence")

        expected = ["<S> HELLO MY DEAR FRIEND </S>", "<S> HOW ARE YOU MY FRIEND </S>"]
        actual = list(ngram.split_corpus_sentences(self.corpus2))

        self.assertEqual(expected, actual, "Split corpus should return two sentences")

    def test_split_sentence_n_grams(self):
        ngram = n_gram.NGram()

        expected = ["<S>",  "HELLO", "MY",  "DEAR",  "FRIEND",  "</S>"]
        actual = list(ngram.split_sentence_n_grams(self.corpus1, 1))

        self.assertEqual(expected, actual, "Split sentence should return list of one words")

        expected = ["<S> HELLO", "HELLO MY", "MY DEAR", "DEAR FRIEND", "FRIEND </S>"]
        actual = list(ngram.split_sentence_n_grams(self.corpus1, 2))

        self.assertEqual(expected, actual, "Split sentence should return list of two words")

    def test_get_top_n_by_counts(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.corpus3)

        actual_top_2= unigram.get_top_n_by_counts(2)
        expected_top_2 = [("THIS", 3), ("MY", 2)]

        self.assertListEqual(expected_top_2, actual_top_2, "Incorrect top 2 elements by counts")

    def test_get_word_occurences(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.corpus1)

        expected = 6
        actual = unigram.get_word_occurences()
        self.assertEqual(expected, actual, "Should return 6 word occurences")

        trigram = n_gram.Trigram()
        trigram.add_corpus(self.corpus2)
        trigram.flush()
        trigram.add_corpus(self.corpus2)

        expected = 13
        actual = trigram.get_word_occurences()
        self.assertEqual(expected, actual, "Should return 13 word occurences")

    def test_discard_unfrequent_n_grams(self):
        unigram = n_gram.Unigram()
        unigram.add_corpus(self.corpus3)

        discarded = unigram.discard_unfrequent_n_grams(1)
        expected_discarded = ["<S>", "IS", "VICTORY", "NIGHT", "</S>"]

        self.assertCountEqual(discarded, expected_discarded,
                              "Should return all n_grams with count less than or equal to 1")

        expected = {"THIS": 3, "MY": 2, "<UNK>": 5}
        actual = unigram.get_counts()

        self.assertDictEqual(expected, actual, "Should discard all n_grams with count less than or equal to 1")

        unigram.flush()
        unigram.add_corpus(self.corpus3)

        unigram.discard_unfrequent_n_grams(2)

        expected = {"THIS": 3, "<UNK>": 7}
        actual = unigram.get_counts()

        self.assertDictEqual(expected, actual, "Should discard all n_grams with count less than or equal to 2")



