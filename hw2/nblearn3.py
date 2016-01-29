import os
import sys
from os.path import join

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a directory.')
    exit()

def tokenize():
    print(path)
    t_root = ''
    for root, sdirs, files in os.walk(path):
#        print('root = ' + root)
#            print('\t- file %s (full path: %s)' % (filename, file_path))
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.startswith('.') or 'fold' not in file_path:
                continue
            words = file_teardown(file_path)
            if 'positive_' in root and 'truthful_' in root:
                update_helper(words, positive, truthful)
            elif 'positive_' in root and 'deceptive_' in root:
                update_helper(words, positive, deceptive)
            elif 'negative_' in root and 'truthful_' in root:
                update_helper(words, negative, truthful)
            elif 'negative_' in root and 'deceptive_' in root:
                update_helper(words, negative, deceptive)

def update_helper(words, category1, category2):
    for word in words:
        if word == '':
            continue
        if word in category1:
            category1[word] += 1
        else:
            category1[word] = 1
        if word in category2:
            category2[word] += 1
        else:
            category2[word] = 1

def file_teardown(file_path):
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    with open(file_path) as f:
        return map(lambda w: w.lower().strip(punct), f.read().split())

positive = {}
negative = {}
truthful = {}
deceptive = {}
tokenize()

print(positive)
