import struct

def read_ptr(data, addr):
    return struct.unpack('<I', data[addr - 0x08000000:addr - 0x08000000 + 4])[0]

def main():
    with open('rr.gba', 'rb') as f:
        data = f.read()
    addresses = {
        'species_names': 0x8000144,
        'base_stats': 0x80001BC,
        'trainer_class_names': 0x811B4B4,
        'trainers': 0x800FC00
    }
    for name, addr in addresses.items():
        ptr = read_ptr(data, addr)
        offset = ptr - 0x08000000
        print(name, hex(ptr), hex(offset))

if __name__ == '__main__':
    main()
