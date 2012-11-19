Polycomp -- Polyline Compression Package
========================================

This package is an implementation of Google's [encoded polyline algorithm
format](https://developers.google.com/maps/documentation/utilities/polylinealgorithm).
The two primary differences between this implementation and the format
described by Google are:

* Zoom level encoding is not supported.
* Arbitrary precision encoding is supported, with `1e5` being the default.

The compression and decompression algorithms exist as both pure Python and
C implementations (via [Cython](http://cython.org/)).

Installation
------------

Cython is not required for installation, so an in-place installation can
be done as follows:

    $ pip install -e git+https://github.com/Mapkin/polycomp/#egg=polycomp
