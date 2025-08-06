#!/usr/bin/env python3
import argparse
import lzma
import pathlib
import sys

def compress(path):
    src = pathlib.Path(path)
    if not src.is_file():
        print(f"Error: source file '{src}' not found.", file=sys.stderr)
        sys.exit(1)
    dst = src.with_suffix(src.suffix + '.xz')
    with src.open('rb') as i, lzma.open(dst, 'wb', preset=9 | lzma.PRESET_EXTREME) as o:
        o.write(i.read())
    print(f"Compressed '{src}' → '{dst}'")

def decompress(path):
    src = pathlib.Path(path)
    if not src.is_file():
        print(f"Error: source file '{src}' not found.", file=sys.stderr)
        sys.exit(1)
    dst = pathlib.Path(src.stem)
    with lzma.open(src, 'rb') as i, dst.open('wb') as o:
        o.write(i.read())
    print(f"Decompressed '{src}' → '{dst}'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compress or decompress files using LZMA (defaults to compress rr.gba)"
    )
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['compress', 'decompress'],
        default='compress',
        help="Operation to perform (default: compress)"
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='rr.gba',
        help="Path to the file (default: rr.gba)"
    )
    args = parser.parse_args()

    if args.mode == 'compress':
        compress(args.path)
    else:
        decompress(args.path)
