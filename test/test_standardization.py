#!/usr/bin/env python3


import unittest
import Standardize


class TestStandardization(unittest.TestCase):
    def setUp(self):
        self.line1 = "Hello my young brother\n"

    def test_process_line(self):
        actual = Standardize.process_line(self.line1)
        expected = "<S> HELLO MY YOUNG BROTHER </S>"
        self.assertEqual(expected, actual, "Error with standardization")