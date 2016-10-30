#!/usr/bin/env python


from __future__ import print_function

from libc.string cimport memset
from libcpp cimport bool

cdef extern from "math.h":
    float powf(float x, float y)


# Writing this piece of the encoder's inner loop as an (almost) pure
# C function results in a 4x speedup.
cdef bytes _encode_number(long num):
    cdef char buf[16]
    cdef Py_ssize_t i = 0

    num <<= 1
    if num < 0:
        num = ~num

    while num >= 0x20:
        buf[i] = (0x20 | (num & 0x1f)) + 63
        i += 1
        num >>= 5

    buf[i] = <char>(num + 63)
    buf[i+1] = 0 # Is this necessary?
    return buf[:i+1]


def compress(polyline, float precision=5, bint flipxy=False):
    compressed = []
    cdef float power = powf(10, precision)
    cdef long n = len(polyline)
    cdef long prev_x = 0
    cdef long prev_y = 0
    cdef long x_trunc
    cdef long y_trunc
    cdef long dx
    cdef long dy

    for i in range(0, n):
        x_trunc = <long>round(polyline[i][0] * power)
        y_trunc = <long>round(polyline[i][1] * power)

        dx = (x_trunc - prev_x)
        dy = (y_trunc - prev_y)

        if not flipxy:
            compressed.append(_encode_number(dx))
            compressed.append(_encode_number(dy))
        else:
            compressed.append(_encode_number(dy))
            compressed.append(_encode_number(dx))

        prev_x = x_trunc
        prev_y = y_trunc

    poly = ''.join(compressed)
    return poly


def decompress(compressed, float precision=5, bint flipxy=False):
    coords = []
    cdef long x_trunc = 0
    cdef long y_trunc = 0
    cdef long dx
    cdef long dy
    cdef long b
    cdef int shift
    cdef long result

    cdef float power = powf(10, precision)
    cdef char* encStr = compressed 
    cdef long length = len(compressed)
    cdef int i = 0

    while i < length:
        b = 0
        shift = 0
        result = 0

        while True:
            b = encStr[i] - 63
            i += 1

            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dx = ~(result >> 1) if result & 1 else result >> 1
        x_trunc += dx

        shift = 0
        result = 0

        while True:
            b = encStr[i] - 63
            i += 1

            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dy = ~(result >> 1) if result & 1 else result >> 1
        y_trunc += dy

        x = float(x_trunc) / power
        y = float(y_trunc) / power 
        if not flipxy:
            coords.append((x, y))
        else:
            coords.append((y, x))

    return coords
