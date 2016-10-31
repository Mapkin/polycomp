import pytest


from polycomp.codec import (
    decompress as decompress_py,
    compress as compress_py,
)
from polycomp.speedups import (
    decompress as decompress_cy,
    compress as compress_cy,
)


COMPRESSED_POLY = '_p~iF~ps|U_ulLnnqC_mqNvxq`@'
COMPRESSED_POLY_REVERSED = '~ps|U_p~iFnnqC_ulLvxq`@_mqN'
DECOMPRESSED_POLY = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]
native_cython = pytest.mark.parametrize("compress, decompress", [
    (compress_py, decompress_py),
    (compress_cy, decompress_cy),
])


@native_cython
def test_compress(compress, decompress):
    enc = compress(DECOMPRESSED_POLY)
    assert enc == COMPRESSED_POLY


@native_cython
def test_decompress(compress, decompress):
    dec = decompress(COMPRESSED_POLY)
    assert dec == DECOMPRESSED_POLY


@native_cython
def test_roundtrip(compress, decompress):
    points = [(35.6, -82.55), (35.59985, -82.55015)]
    enc = compress(points)
    dec = decompress(enc)
    assert dec == points


@native_cython
def test_compress_reversed(compress, decompress):
    enc = compress(DECOMPRESSED_POLY, flipxy=True)
    assert enc == COMPRESSED_POLY_REVERSED


@native_cython
def test_decompress_reversed(compress, decompress):
    dec = decompress(COMPRESSED_POLY, flipxy=True)
    assert dec == [x[::-1] for x in DECOMPRESSED_POLY]
