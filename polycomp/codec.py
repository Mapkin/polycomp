#!/usr/bin/env python

import math


def compress(polyline, precision=5):
    def encode_number(num):
        """Base64-encode a signed number."""
        num = num << 1
        if num < 0:
            num = ~num

        s = []
        while num >= 0x20:
            s.append(chr((0x20 | (num & 0x1f)) + 63))
            num >>= 5
        s.append(chr(num + 63))
        print(len(s))
        return ''.join(s)

    compressed = []
    precision = 10 ** precision
    prev_x = 0
    prev_y = 0

    for point in polyline:
        x_trunc = int(math.floor(point[0] * precision))
        y_trunc = int(math.floor(point[1] * precision))

        # Encode the difference between the coordinates.
        compressed.append(encode_number(x_trunc - prev_x))
        compressed.append(encode_number(y_trunc - prev_y))

        prev_x = x_trunc
        prev_y = y_trunc

    poly = ''.join(compressed)
    return poly.replace('\\', '\\\\')


def decompress(compressed, precision=5):
    coords = []
    precision = 10 ** precision
    x = 0
    y = 0
    i = 0

    while i < len(compressed):
        b = 0
        shift = 0
        result = 0

        while True:
            b = ord(compressed[i]) - 63
            i += 1

            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dx = ~(result >> 1) if result & 1 else result >> 1
        x += dx

        shift = 0
        result = 0

        while True:
            b = ord(compressed[i]) - 63
            i += 1

            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dy = ~(result >> 1) if result & 1 else result >> 1
        y += dy

        coords.append((float(x) / precision, float(y) / precision))

    return coords
