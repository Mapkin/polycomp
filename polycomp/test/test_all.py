#!/usr/bin/env python


import unittest

from polycomp import (
    decompress,
    compress,
)


COMPRESSED_POLY = '_p~iF~ps|U_ulLnnqC_mqNvxq`@'
DECOMPRESSED_POLY = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]


class CompressionTestCase(unittest.TestCase):
    def runTest(self):
        enc = compress(DECOMPRESSED_POLY)
        self.assertEqual(enc, COMPRESSED_POLY)


class DecompressionTestCase(unittest.TestCase):
    def runTest(self):
        dec = decompress(COMPRESSED_POLY)
        self.assertEqual(dec, DECOMPRESSED_POLY)
