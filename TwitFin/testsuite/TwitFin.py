#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `TwitFin` module."""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)

from .. import TwitFin

from . import unittest


class twitfinTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def test_something_docstring(self):
        """Here is a sample test with a docstring. Hey."""
        self.assertTrue(True)

    def tearDown(self):
        pass


def suite():
    from .helpers import setup_path
    setup_path()
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(twitfinTestCase))
    return suite
