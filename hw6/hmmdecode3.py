import pickle
import numpy as np

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

p = ''
with open('hmmmodel.txt', 'rb') as rfile:
    global p
    p = pickle.load(rfile)
    print(p)

tag_set = p.keys()
tag_set_size = len(tag_set) - 1

with open(path, 'r') as rfile:
    for line in rfile.readlines():
        if not line.strip():
            continue
        line_segs = line.strip().split(' ')

prob = np.zero((tag_set_size, tag_set_size), dtype=float64)
backp = []
