import pickle
import numpy as np
import sys
import os

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

print(tag_map)

with open(path, 'r') as rfile:
    for line in rfile.readlines():
        if not line.strip():
            continue
        line_segs = line.strip().split(' ')
        print(line_segs)
        T = len(line_segs)
        print(T)
        prob = np.zeros((tag_set_size, T), dtype=np.float64)
        backp = np.zeros((tag_set_size, T), dtype=np.float64)
        
        # Initialization step
        for tag in tag_set:
            print(tag)
            obs_p = 1
            if line_segs[0] in p[tag]['words']:
                obs_p = p[tag]['words'][line_segs[0]].log10()
            prob[tag_map[tag]][0] = p[tag]['tags'][start_state].log10() + obs_p

        # Filling the rest
        for t in range(1, T):
            for tag1 in tag_set:
                for tag2 in tag_set:
                obs_p = 1
                if line_segs[t] in p[tag]['words']:
                    obs_p = p[tag]['words'][line_segs[t]].log10()
                prob[tag_map[tag]][t] = p[tag]['tags'][tag].log10() + obs_p
               

        print(prob)
