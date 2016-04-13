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

#for t in tag_set:
#    sum = 0
#    for w in list(p[t]['words'].keys()):
#        sum += p[t]['words'][w]
#    print('sum for', t, ' is: ', sum)
#

#for t1 in tag_set:
#    sum = 0
#    for t2 in tag_set:
#        sum += p[t2]['tags'][t1]
#    print('sum for', t2, 'given', t1,'is:', sum)

wfile = open('hmmoutput.txt', 'w')
with open(path, 'r') as rfile:
    for line in rfile.readlines():
        if not line.strip():
            continue
        line_segs = line.strip().split(' ')
        T = len(line_segs)
        prob = np.zeros((tag_set_size, T), dtype=Decimal)
        backp = np.zeros((tag_set_size, T), dtype=np.int)
        
        # Initialization step
        for tag in tag_set:
            if line_segs[0] in p[tag]['words']:
                obs_p = p[tag]['words'][line_segs[0]]
                prob[tag_map[tag]][0] = p[tag]['tags'][start_state].log10() + obs_p.log10()
            else:
                prob[tag_map[tag]][0] = p[tag]['tags'][start_state].log10() -999
            backp[tag_map[tag]][0] = tag_map[start_state]

        # Filling the rest
        for t in range(1, T):
            for tag1 in tag_set:
                max_val = float('-inf')
                max_tag = -1
                for tag2 in tag_set:
                    temp = p[tag1]['tags'][tag2].log10() + prob[tag_map[tag2]][t-1]
                    if line_segs[t] in p[tag1]['words']:
                        obs_p = p[tag1]['words'][line_segs[t]].log10()
                        temp += obs_p
                    else:
                        temp -= 999
                    if max_val < temp:
                        max_val = temp
                        max_tag = tag_map[tag2]

                prob[tag_map[tag1]][t] = max_val
                backp[tag_map[tag1]][t] = max_tag

        res = []
        max_pos = -1
        max_val = float('-inf')
        for tag in tag_set:
            if prob[tag_map[tag]][T-1] > max_val:
                max_val = prob[tag_map[tag]][T-1]
                max_pos = tag_map[tag]
        res.append(max_pos)

        for x in range(T-1, -1, -1):
            max_pos = backp[max_pos][x]
            res.append(max_pos)

        res.reverse()
#        print('len res is', len(res))

        for index, tag_num in enumerate(res[1:]):
            wfile.write(line_segs[index] + '/' + list(tag_map.keys())[list(tag_map.values()).index(tag_num)] + ' ')
        wfile.write('\n')

wfile.close()
