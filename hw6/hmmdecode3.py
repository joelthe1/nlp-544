import pickle
import numpy as np
import sys
import os
from decimal import *

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

with open('hmmmodel.txt', 'rb') as rfile:
    global p
    p = pickle.load(rfile)
#    print(p)

start_state = '<~s~>'
tag_set = p.keys()
tag_set_size = len(tag_set)
tag_map = {}
for index, tag in enumerate(tag_set):
    tag_map[tag] = index

#tag_map = {'<~s~>': 0, 'DT': 1, 'IN': 2, 'VB': 3, 'NN': 4}

#print(tag_map)

with open(path, 'r') as rfile:
    for line in rfile.readlines():
        if not line.strip():
            continue
        line_segs = line.strip().split(' ')
        print(line_segs)
        T = len(line_segs)
        print(T)
        prob = np.zeros((tag_set_size, T), dtype=Decimal)
        backp = np.zeros((tag_set_size, T), dtype=np.int)
        
        # Initialization step
        for tag in tag_set:
            if line_segs[0] in p[tag]['words']:
                obs_p = p[tag]['words'][line_segs[0]].log10() * -1
                prob[tag_map[tag]][0] = (p[tag]['tags'][start_state].log10() * -1) + obs_p
            else:
                prob[tag_map[tag]][0] = p[tag]['tags'][start_state].log10() * -1
            backp[tag_map[tag]][0] = tag_map[start_state]

        # Filling the rest
        for t in range(1, T):
            for tag1 in tag_set:
                min_val = float('inf')
                min_tag = -1
                for tag2 in tag_set:
                    temp = (p[tag1]['tags'][tag2].log10() * -1) + prob[tag_map[tag2]][t-1]
                    if line_segs[t] in p[tag1]['words']:
                        obs_p = p[tag1]['words'][line_segs[t]].log10() * -1
                        temp += obs_p
                    if min_val > temp:
                        min_val = temp
                        min_tag = tag_map[tag2]

                prob[tag_map[tag1]][t] = min_val
                backp[tag_map[tag1]][t] = min_tag

        res = []
        min_pos = -1
        min_val = float('inf')
        for tag in tag_set:
            if prob[tag_map[tag]][T-1] < min_val:
                min_val = prob[tag_map[tag]][T-1]
                min_pos = tag_map[tag]
        res.append(min_pos)

        for x in range(T-1, -1, -1):
            min_pos = backp[min_pos][x]
            res.append(min_pos)

        res.reverse()
        for value in res:
            print(list(tag_map.keys())[list(tag_map.values()).index(value)])

