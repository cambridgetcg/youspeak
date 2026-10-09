#!/usr/bin/env python3
"""pngpeek.py FILE.png x,y [x,y …] — print RGBA at pixels (stdlib PNG decoder,
8-bit RGB/RGBA, non-interlaced). Verification aid only; never draws."""
import struct
import sys
import zlib


def decode(path):
    b = open(path, "rb").read()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    i, idat, w = 8, b"", None
    while i < len(b):
        n, t = struct.unpack(">I4s", b[i:i + 8])
        d = b[i + 8:i + 8 + n]
        if t == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", d)
            assert depth == 8 and ctype in (2, 6) and inter == 0, (depth, ctype, inter)
            bpp = 4 if ctype == 6 else 3
        elif t == b"IDAT":
            idat += d
        i += 12 + n
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows, prev, p = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[p]; line = bytearray(raw[p + 1:p + 1 + stride]); p += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            c = prev[x - bpp] if x >= bpp else 0
            up = prev[x]
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + up) & 255
            elif f == 3: line[x] = (line[x] + ((a + up) >> 1)) & 255
            elif f == 4:
                pa, pb, pc = abs(up - c), abs(a - c), abs(a + up - 2 * c)
                pr = a if pa <= pb and pa <= pc else (up if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(line); prev = line
    return w, h, bpp, rows


if __name__ == "__main__":
    w, h, bpp, rows = decode(sys.argv[1])
    for xy in sys.argv[2:]:
        x, y = map(int, xy.split(","))
        px = tuple(rows[y][x * bpp:(x + 1) * bpp])
        print(f"{x},{y}: #" + "".join(f"{v:02x}" for v in px[:3]) + (f" a={px[3]}" if bpp == 4 else ""))
