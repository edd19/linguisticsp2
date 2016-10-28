#!/usr/bin/env python3

import unittest
import estimation_n_grams


class TestNGram(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"
        self.corpus3 = "<s> THIS THIS IS MY MY VICTORY THIS NIGHT </s>"

    def test_estimate_unigram(self):
        max_likelihood = estimation_n_grams.MaxLikelihood(1)

        max_likelihood.add_training_corpus(self.corpus1)

        one_gram = "HELLO"
        probability = max_likelihood.estimate_n_gram(one_gram)
        expected_probability = 1/6
        self.assertEqual(probability, expected_probability, "Don't return good probability")

        max_likelihood.flush()
        max_likelihood.add_training_corpus(self.corpus3)

        one_gram = "HELLO"
        probability = max_likelihood.estimate_n_gram(one_gram)
        expected_probability = 0
        self.assertEqual(probability, expected_probability, "Word not present should return 0")

        one_gram = "THIS"
        probability = max_likelihood.estimate_n_gram(one_gram)
        expected_probability = 3/10
        self.assertEqual(probability, expected_probability, "Don't return good probability")

    def test_get_minus_n_gram(self):
        max_likelihood = estimation_n_grams.MaxLikelihood
        two_gram = "HELLO MY"
        expected = "HELLO"
        actual = max_likelihood.get_minus_n_gram(two_gram)

        self.assertEqual(expected, actual, "Should return a reduce a one_gram")

        four_gram = "HELLO MY DEAR FRIEND"
        expected = "HELLO MY DEAR"
        actual = max_likelihood.get_minus_n_gram(four_gram)

        self.assertEqual(expected, actual, "Should return a reduce a three_gram")