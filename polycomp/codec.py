import itertools


def compress(polyline, precision=5, flipxy=False, deltas=False):
    """
    Compute the polyline compressed representation for a list of coordinates

    Parameters
    ----------
    polyline : list of list of floats
    precision : int
        Number of significant figures for rounding coordinates
    flipxy : optional (default True)
        Flip the coordinate order in the output.
        This should be True when coordinates are passed in as lon, lat
    deltas : optional (default False)
        Specifies whether the input polyline is already truncated and delta-encoded

    """
    compressed = []

    if not deltas:
        points = delta_encode(polyline, precision)
    else:
        points = polyline

    for x_delta, y_delta in points:
        x = encode_number(x_delta)
        y = encode_number(y_delta)
        if flipxy:
            x, y = y, x
        compressed.extend(x)
        compressed.extend(y)

    poly = ''.join(compressed)
    return poly


def decompress(compressed, precision=5, flipxy=False):
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
        
        a, b = x, y
        if flipxy:
            a, b = b, a
        coords.append((float(a) / precision, float(b) / precision))

    return coords


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
    return s


def delta_encode(polyline, precision):
    prev_x, prev_y = 0, 0
    precision = 10 ** precision
    for p in polyline:
        x = long(round(p[0] * precision))
        y = long(round(p[1] * precision))

        delta_x = x - prev_x
        delta_y = y - prev_y
        
        yield delta_x, delta_y

        prev_x, prev_y = x, y
