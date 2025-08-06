import struct
import sys

def read_ptr(data, addr):
    off = addr - 0x08000000
    return struct.unpack('<I', data[off:off + 4])[0]

def scan(path):
    with open(path, 'rb') as f:
        data = f.read()
    addresses = {
        'species_names': 0x8000144,
        'base_stats': 0x80001BC,
        'trainer_class_names': 0x811B4B4,
        'trainers': 0x800FC00
    }
    for name, addr in addresses.items():
        ptr = read_ptr(data, addr)
        if 0x08000000 <= ptr < 0x08000000 + len(data):
            offset = ptr - 0x08000000
            print(name, f'{ptr:#010x}', f'{offset:#010x}')
        else:
            print(name, 'invalid')

if __name__ == '__main__':
    scan(sys.argv[1] if len(sys.argv) > 1 else 'rr.gba')
