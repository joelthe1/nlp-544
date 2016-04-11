import sys
import os
import re
from decimal import *
import numpy as np

mapping = {}
path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

def separate(token):
    patt = re.compile(r'(.*)\/([A-Z0-9]{2})')
    res = patt.match(token)
    #TODO: if res: for safety
    word = res.group(1)
    tag = res.group(2)
    return {'word': word, 'tag': tag}

def tokenize():
    print(path)
    with open(path, 'r') as rfile:
        for line in rfile.readlines():
            if not line.strip():
                continue
            line_segs = line.strip().split(' ')
            prev = {'tag': '<~s~>'}

            for seg in line_segs:
                token = separate(seg)
                insert(prev, token)
                prev = token
#    print mapping

def insert(prev, curr):
    global mapping
    if curr['tag'] not in mapping:
        mapping[curr['tag']] = {}
        mapping[curr['tag']]['tags'] = {prev['tag']: 1}
        mapping[curr['tag']]['words'] = {curr['word']: 1}
        mapping[curr['tag']]['emmis_denom'] = 1
    else:
        if prev['tag'] in mapping[curr['tag']]['tags']:
            mapping[curr['tag']]['tags'][prev['tag']] += 1
        else:
            mapping[curr['tag']]['tags'][prev['tag']] = 1

        if curr['word'] in mapping[curr['tag']]['words']:
            mapping[curr['tag']]['words'][curr['word']] += 1
        else:
            mapping[curr['tag']]['words'][curr['word']] = 1
        mapping[curr['tag']]['emmis_denom'] += 1

    if prev['tag'] not in mapping:
        mapping[prev['tag']] = {}
        mapping[prev['tag']] = {}
        mapping[prev['tag']]['tags'] = {}
        mapping[prev['tag']]['words'] = {}

    if 'trans_denom' not in mapping[prev['tag']]:
        mapping[prev['tag']]['trans_denom'] = 1
    else:
        mapping[prev['tag']]['trans_denom'] += 1

def calc_p():
    p = {}
    tag_set = mapping.keys()
    tag_set_size = len(tag_set)
    print(tag_set)
    for tag1 in tag_set:
        print('tag1'+tag1)        
        p[tag1] = {'tags':{}, 'words':{}}
        for tag2 in tag_set:
            print(tag2)
            numer = 1
            denom = 0
            if tag2 in mapping[tag1]['tags']:
                numer = mapping[tag1]['tags'][tag2] + 1
            p_t1_gvn_t2 = Decimal(numer)/(Decimal(mapping[tag2]['trans_denom'])+Decimal(tag_set_size))
            p[tag1]['tags'][tag2] = np.log(p_t1_gvn_t2) * -1
        for word in mapping[tag1]['words'].keys():
            p_w_gvn_t1 = Decimal(mapping[tag1]['words'][word])/Decimal(mapping[tag1]['emmis_denom'])
            p[tag1]['words'][word] = np.log(p_w_gvn_t1) * -1
    print(p)

tokenize()
calc_p()
