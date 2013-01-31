#!/usr/bin/env python


from __future__ import print_function

from libc.string cimport memset

cdef extern from "math.h":
    float powf(float x, float y)


# Writing this piece of the encoder's inner loop as an (almost) pure
# C function results in a 4x speedup.
cdef bytes _encode_number(int num):
    cdef char buf[5]
    cdef Py_ssize_t i = 0

    num <<= 1
    if num < 0:
        num = ~num

    memset(buf, 0, 5)
    while num >= 0x20:
        buf[i] = (0x20 | (num & 0x1f)) + 63
        i += 1
        num >>= 5

    buf[i] = <char>(num + 63)
    return buf[:i+1]


def compress(polyline, float precision=5):
    compressed = []
    cdef float power = powf(10, precision)
    cdef long n = len(polyline)
    cdef long prev_x = 0
    cdef long prev_y = 0
    cdef long x_trunc
    cdef long y_trunc
    cdef int dx
    cdef int dy

    for i in range(0, n):
        x_trunc = <long>round(polyline[i][0] * power)
        y_trunc = <long>round(polyline[i][1] * power)

        dx = <int>(x_trunc - prev_x)
        compressed.append(_encode_number(dx))

        dy = <int>(y_trunc - prev_y)
        compressed.append(_encode_number(dy))

        prev_x = x_trunc
        prev_y = y_trunc

    poly = ''.join(compressed)
    return poly


def decompress(compressed, float precision=5):
    coords = []
    cdef long x_trunc = 0
    cdef long y_trunc = 0
    cdef long dx
    cdef long dy
    cdef int b
    cdef int shift
    cdef int result

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
        coords.append((x, y))

    return coords

