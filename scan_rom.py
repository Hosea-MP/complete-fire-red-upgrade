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
    results = {}
    for name, addr in addresses.items():
        ptr = read_ptr(data, addr)
        if 0x08000000 <= ptr < 0x08000000 + len(data):
            offset = ptr - 0x08000000
            results[name] = f"{name} {ptr:#010x} {offset:#010x}\n"
        else:
            results[name] = f"{name} invalid\n"
    with open('pokemon_tables.txt', 'w') as f:
        f.write(results['species_names'])
        f.write(results['base_stats'])
    with open('trainer_tables.txt', 'w') as f:
        f.write(results['trainer_class_names'])
        f.write(results['trainers'])

if __name__ == '__main__':
    scan(sys.argv[1] if len(sys.argv) > 1 else 'rr.gba')
