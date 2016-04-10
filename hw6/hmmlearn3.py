import sys
import os
import re

mapping = {}
path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

def tokenize():
    print(path)
    pat = re.compile(r'(.*?)\/([A-Z0-9]{2})')
    with open(path, 'r') as rfile:
        for line in rfile.readlines():
#            print line
            line_segs = line.strip().split(' ')
            res = pat.match(segs)
            #TODO: if res: for safety
            word = res.group(1)
            tag = res.group(2)
            if tag not in mapping:
                mapping[tag] = {}
                mapping[tag]['tags'] = {'<~s~>': 1}
                mapping[tag]['words'] = {word: 1}
                mapping[tag]['trans_denom'] = 1
                mapping[tag]['emmis_denom'] = 1
            prev = (word, tag)

            for segs in line_segs[1:-1]:
                res = pat.match(segs)
                print(line_segs)
                word = res.group(1)
                tag = res.group(2)
                mapping[tag]['trans_denom'] += 1
                mapping[tag]['emmis_denom'] += 1
                if prev[1] not in mapping[tag]['tags']:
                    mapping[tag]['tags'][prev[1]] = 1
                else:
                    mapping[tag]['tags'][prev[1]] += 1

                if prev[2] not in mapping[tag]['words']:
                    mapping[tag]['words'] = 1
                else:
                    mapping[tag]['words'] += 1
                prev = (word, tag)

                

#    for root, sdirs, files in os.walk(path):
#        for filename in files:
#            file_path = os.path.join(root, filename)
#            if filename.startswith('.') or filename == 'LICENSE' or filename == 'README.txt':
#                continue

            
            
tokenize()
