import mmap,struct

def r(addr):
    return addr-0x08000000

def p(buf,addr):
    return struct.unpack_from('<I',buf,addr)[0]-0x08000000

def main():
    with open('test.gba','rb') as f:
        rom=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        base=p(rom,0x1BC)
        pattern=bytes([45,49,49,45,65,65,2,3,45,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        first=rom.find(pattern,base,base+0x1000)
        trainers=r(0x823EAC8)
        party,cls=struct.unpack_from('<BB',rom,trainers)
        print(hex(first),hex(trainers),party,cls)
if __name__=='__main__':
    main()
