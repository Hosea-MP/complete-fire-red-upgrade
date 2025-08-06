import argparse
import lzma
import pathlib

def compress(path):
    src = pathlib.Path(path)
    dst = src.with_suffix(src.suffix + '.xz')
    with src.open('rb') as i, lzma.open(dst, 'wb', preset=9 | lzma.PRESET_EXTREME) as o:
        o.write(i.read())

def decompress(path):
    src = pathlib.Path(path)
    dst = pathlib.Path(src.stem)
    with lzma.open(src, 'rb') as i, dst.open('wb') as o:
        o.write(i.read())

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['compress', 'decompress'])
    p.add_argument('path')
    a = p.parse_args()
    if a.mode == 'compress':
        compress(a.path)
    else:
        decompress(a.path)
