import sys
import os
import re
from decimal import *

mapping = {}
path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

def separate(token):
    patt = re.compile(r'(.*?)\/([A-Z0-9]{2})')
    res = patt.match(token)
    #TODO: if res: for safety
    word = res.group(1)
    tag = res.group(2)
    return {'word': word, 'tag': tag}

def tokenize():
    print(path)
    with open(path, 'r') as rfile:
        for line in rfile.readlines():
            print(line)
            if not line.strip():
                continue
            line_segs = line.strip().split(' ')
            prev = {'tag': '<~s~>'}

            for seg in line_segs:
                token = separate(seg)
                insert(prev, token)
                prev = token
    print mapping

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

    if 'trans_denom' not in mapping[prev['tag']]:
        mapping[prev['tag']]['trans_denom'] = 1
    else:
        mapping[prev['tag']]['trans_denom'] += 1

tokenize()
