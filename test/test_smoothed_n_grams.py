#!/usr/bin/env python3

import unittest
from smoothed_n_grams import LaplaceSmoothing


class TestLaplaceSmoothing(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"
        self.corpus3 = "<s> THIS THIS IS MY MY VICTORY THIS NIGHT </s>"
        self.corpus4 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY DEAR FRIEND MY MY </s>"

    def test_estimation_unigram(self):
        laplace = LaplaceSmoothing(1)

        laplace.add_training_corpus(self.corpus1)

        actual = laplace.estimate_n_gram("HELLO")
        expected = 2/12
        self.assertEqual(expected, actual, "Don't return good probability")

        actual = laplace.estimate_n_gram("YOUNG")
        expected = 1/12
        self.assertEqual(expected, actual, "Don't return good probability")

    def test_estimation_trigram(self):
        laplace = LaplaceSmoothing(3)

        laplace.add_training_corpus(self.corpus2)

        actual = laplace.estimate_n_gram("HELLO MY DEAR")
        expected = 2 / 10
        self.assertEqual(expected, actual, "Don't return good probability")

        laplace.flush()
        laplace.add_training_corpus(self.corpus4)

        actual = laplace.estimate_n_gram("MY DEAR FRIEND")
        expected = 3 / 11
        self.assertEqual(expected, actual, "Don't return good probability")
