import pickle
import sys
import os
from decimal import *
import codecs

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

with open('hmmmodel.txt', 'rb') as rfile:
    global p
    p = pickle.load(rfile)
#    print(p)

vocab = p['vocab']
del p['vocab']
start_state = '<~s~>'
tag_set = p.keys()
tag_set_size = len(tag_set)
tag_map = {}
for index, tag in enumerate(tag_set):
    tag_map[tag] = index

output = []

with codecs.open(path, 'r', 'utf-8') as rfile:
    lines = rfile.readlines()

for line in lines:
    if not line.strip():
        continue
    line_segs = line.strip().split(' ')
    T = len(line_segs)
    bp = {}
    previous = {start_state: Decimal(0.0)}

    for index, word in enumerate(line_segs):
        curr = {}
        bp[index] = {}
        for cur_s in tag_set:
            if cur_s == start_state:
                continue
            if word in vocab and word not in p[cur_s]['words']:
                continue
                
            max_value = Decimal(float("-inf"))
            temp_bp = None
            for prev_s in previous:
                prev_p = Decimal(previous[prev_s])
                transition_p = p[cur_s]['tags'][prev_s].log10()
                if word in vocab:
                    emission_p = p[cur_s]['words'][word].log10()
                    prob = prev_p + transition_p + emission_p
                else:
                    prob = prev_p + transition_p
                if prob > max_value:
                    max_value = prob
                    temp_bp = prev_s

            curr[cur_s] = max_value
            bp[index][cur_s] = temp_bp

        previous = curr
    
    tag = ""
    max = float("-inf")
    for state in previous:
        if previous[state] > max:
            tag = state
            
    tag_sequence = []
    for x in range(T-1, -1, -1):
        word = line_segs[x]
        tag_sequence.append(tag)
        tag = bp[x][tag]
    tag_sequence.reverse()

    outline = []
    for index, tag in enumerate(tag_sequence):
        l = line_segs[index] + '/' + tag
        outline.append(l)
    tempval = ' '.join(outline) + '\n'
    output.append(tempval)

with codecs.open('hmmoutput.txt', 'w', 'utf-8') as wfile:
    for lines in output:
        wfile.write(lines)
