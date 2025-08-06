import argparse
import lzma
import json
import struct


def read_charmap(path):
    d={}
    with open(path,encoding='utf-8-sig') as f:
        for line in f:
            line=line.strip()
            if not line or '=' not in line:
                continue
            k,v=line.split('=',1)
            d[int(k,16)]=v
    return d


def decode(data,pos,table):
    chars=[]
    while pos<len(data):
        b=data[pos]
        pos+=1
        if b==255:
            break
        chars.append(table.get(b,'?'))
    return ''.join(chars),pos


def read_table_file(path):
    d={}
    with open(path) as f:
        for line in f:
            parts=line.split()
            if len(parts)==3:
                d[parts[0]]=int(parts[2],16)
    return d


def read_species(data,offsets,table,count):
    names=[]
    pos=offsets['species_names']
    for _ in range(count):
        s,pos=decode(data,pos,table)
        names.append(s)
    return names


def read_base_stats(data,offsets,count):
    stats=[]
    off=offsets['base_stats']
    for i in range(count):
        hp,atk,defn,spd,spa,spd2=struct.unpack_from('<6B',data,off+i*28)
        stats.append({'hp':hp,'attack':atk,'defense':defn,'speed':spd,'sp_attack':spa,'sp_defense':spd2})
    return stats


def read_trainer_classes(data,offsets,table):
    names=[]
    pos=offsets['trainer_class_names']
    end=offsets['trainers']
    while pos<end:
        s,pos=decode(data,pos,table)
        if not s:
            break
        names.append(s)
    return names


def decode_fixed_name(bs,table):
    s=''
    for b in bs:
        if b==255:
            break
        s+=table.get(b,'?')
    return s


def read_trainers(data,offsets,class_names,table):
    trainers=[]
    pos=offsets['trainers']
    size=40
    while pos+size<=len(data):
        pf=data[pos]
        tc=data[pos+1]
        emg=data[pos+2]
        tp=data[pos+3]
        name=decode_fixed_name(data[pos+4:pos+16],table)
        items=list(struct.unpack_from('<4H',data,pos+16))
        db=data[pos+24]
        ai=struct.unpack_from('<I',data,pos+28)[0]
        ps=data[pos+32]
        party_ptr=struct.unpack_from('<I',data,pos+36)[0]
        if pf==0 and tc==0 and emg==0 and tp==0 and not name and items==[0,0,0,0] and db==0 and ai==0 and ps==0 and party_ptr==0:
            break
        trainer={'class':class_names[tc] if tc<len(class_names) else tc,'name':name,'party_size':ps,'party_pointer':party_ptr}
        trainers.append(trainer)
        pos+=size
    return trainers


def main(path,count):
    table=read_charmap('charmap.tbl')
    p_offsets=read_table_file('tables/pokemon_tables.txt')
    t_offsets=read_table_file('tables/trainer_tables.txt')
    if path.endswith('.xz'):
        data=lzma.open(path,'rb').read()
    else:
        data=open(path,'rb').read()
    names=read_species(data,p_offsets,table,count)
    stats=read_base_stats(data,p_offsets,count)
    pokemon=[{'name':names[i],'stats':stats[i]} for i in range(count)]
    class_names=read_trainer_classes(data,t_offsets,table)
    trainers=read_trainers(data,t_offsets,class_names,table)
    json.dump(pokemon,open('pokemon_data.json','w'))
    json.dump({'classes':class_names,'trainers':trainers},open('trainer_data.json','w'))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('path',nargs='?',default='rr.gba.xz')
    ap.add_argument('--count',type=int,default=412)
    args=ap.parse_args()
    main(args.path,args.count)
