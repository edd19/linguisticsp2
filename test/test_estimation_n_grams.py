#!/usr/bin/env python3

import estimation_n_grams
import unittest


class TestLinearInterpolation(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"
        self.corpus3 = "<s> THIS THIS IS MY MY VICTORY THIS NIGHT </s>"
        self.corpus4 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY DEAR FRIEND MY MY </s>"

    def test_create_n_grams_array(self):
        linear_interpolation = estimation_n_grams.LinearInterpolation(n=1, k=1)

        actual = [x.n for x in linear_interpolation.n_grams_array]
        expected = [1]

        self.assertCountEqual(expected, actual, "Should create one n_gram object")

        linear_interpolation = estimation_n_grams.LinearInterpolation(n=3, k=3)

        actual = [x.n for x in linear_interpolation.n_grams_array]
        expected = [1, 2, 3]

        self.assertCountEqual(expected, actual, "Should create three n_gram objects")

        linear_interpolation = estimation_n_grams.LinearInterpolation(n=5, k=3)

        actual = [x.n for x in linear_interpolation.n_grams_array]
        expected = [2, 3, 4, 5]

        self.assertCountEqual(expected, actual, "Should create four n_gram objects")

    def test_estimate_unigram(self):
        linear_interpolation = estimation_n_grams.LinearInterpolation(n=1, k=1)

        linear_interpolation.add_training_corpus(self.corpus1)

        probability = linear_interpolation.estimate_n_gram("HELLO")
        expected_probability = 1 / 6
        self.assertEqual(probability, expected_probability, "Don't return good probability")

        probability = linear_interpolation.estimate_n_gram("PRESENT")
        expected_probability = 0
        self.assertEqual(probability, expected_probability, "Should return 0 as word is not present")

    def test_estimate_bigram(self):
        linear_interpolation = estimation_n_grams.LinearInterpolation(n=2, k=2)

        linear_interpolation.add_training_corpus(self.corpus3)

        probability = linear_interpolation.estimate_n_gram("THIS IS")
        expected_probability = 13 / 60
        self.assertEqual(probability, expected_probability, "Don't return good probability")

    def test_estimate_trigram(self):
        linear_interpolation = estimation_n_grams.LinearInterpolation(n=3, k=1)

        linear_interpolation.add_training_corpus(self.corpus1)

        probability = linear_interpolation.estimate_n_gram("HELLO MY DEAR")
        expected_probability = 1 / 1
        self.assertEqual(probability, expected_probability, "Don't return good probability")

        linear_interpolation = estimation_n_grams.LinearInterpolation(n=3, k=2)
        linear_interpolation.add_training_corpus(self.corpus4)

        probability = linear_interpolation.estimate_n_gram("MY DEAR FRIEND")
        expected_probability = 1
        self.assertEqual(probability, expected_probability, "Don't return good probability")

    def test_reduce_sentence(self):
        linear_interpolation = estimation_n_grams.LinearInterpolation(n=1, k=1)

        actual = linear_interpolation.reduce_sentence(self.corpus1)
        expected = "HELLO MY DEAR FRIEND </s>"
        self.assertEqual(expected, actual, "Should only remove first word")


class TestMaximumLikelihood(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"
        self.corpus3 = "<s> THIS THIS IS MY MY VICTORY THIS NIGHT </s>"
        self.corpus4 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY DEAR FRIEND MY MY </s>"

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

    def test_estimate_bigram(self):
        max_likelihood = estimation_n_grams.MaxLikelihood(n=2)

        max_likelihood.add_training_corpus(self.corpus1)

        bi_gram = "HELLO MY"
        probability = max_likelihood.estimate_n_gram(bi_gram)
        expected_probability = 1/1
        self.assertEqual(probability, expected_probability, "Don't return good probability")

        bi_gram = "HELLO YOU"
        probability = max_likelihood.estimate_n_gram(bi_gram)
        expected_probability = 0
        self.assertEqual(probability, expected_probability, "Don't return good probability")

        max_likelihood.flush()
        max_likelihood.add_training_corpus(self.corpus4)

        bi_gram = "MY DEAR"
        probability = max_likelihood.estimate_n_gram(bi_gram)
        expected_probability = 2 / 4
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


class TestLaplaceSmoothing(unittest.TestCase):
    def setUp(self):
        self.corpus1 = "<s> HELLO MY DEAR FRIEND </s>"
        self.corpus2 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY FRIEND </s>"
        self.corpus3 = "<s> THIS THIS IS MY MY VICTORY THIS NIGHT </s>"
        self.corpus4 = "<s> HELLO MY DEAR FRIEND </s>\n<s> HOW ARE YOU MY DEAR FRIEND MY MY </s>"

    def test_estimation_unigram(self):
        laplace = estimation_n_grams.LaplaceSmoothing(1)

        laplace.add_training_corpus(self.corpus1)

        actual = laplace.estimate_n_gram("HELLO")
        expected = 2/12
        self.assertEqual(expected, actual, "Don't return good probability")

        actual = laplace.estimate_n_gram("YOUNG")
        expected = 1/12
        self.assertEqual(expected, actual, "Don't return good probability")

    def test_estimation_trigram(self):
        laplace = estimation_n_grams.LaplaceSmoothing(3)

        laplace.add_training_corpus(self.corpus2)

        actual = laplace.estimate_n_gram("HELLO MY DEAR")
        expected = 2 / 10
        self.assertEqual(expected, actual, "Don't return good probability")

        laplace.flush()
        laplace.add_training_corpus(self.corpus4)

        actual = laplace.estimate_n_gram("MY DEAR FRIEND")
        expected = 3 / 11
        self.assertEqual(expected, actual, "Don't return good probability")