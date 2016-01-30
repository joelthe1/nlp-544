from decimal import Decimal
import sys
import os
from math import log

path = sys.argv[1]
def file_teardown(file_path):
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'
    with open(file_path) as f:
        return map(lambda w: w.lower().strip(punct), f.read().split())

def tokenizeClassify():
    for root, sdirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.startswith('.') or 'fold' not in file_path:
                continue
            words = file_teardown(file_path)
            classify(words, file_path)

def classify(words, file_path):
    score = {}
    score['p'] = log(p_positive)
    score['n'] = log(p_negative)
    score['t'] = log(p_truthful)
    score['d'] = log(p_deceptive)

    for word in words:
        if word in condProb:
            score['p'] += log(condProb[word]['p'])
            score['n'] += log(condProb[word]['n'])
            score['t'] += log(condProb[word]['t'])
            score['d'] += log(condProb[word]['d'])
    if score['t'] > score['d']:
        wfile.write('truthful ')
    else:
        wfile.write('deceptive ')
        
    if score['p'] > score['n']:
        wfile.write('positive ')
    else:
        wfile.write('negative ')

    wfile.write(file_path + '\n')

def setup():
    global p_positive, p_negative, p_truthful, p_deceptive
    with open('nbmodel.txt', 'r') as f:
        priors = f.readline().strip().split('|')
        print(priors)
        for prior in priors:
            val = prior.split(':')
            if val[0] == 'p':
                p_positive = Decimal(val[1])
            elif val[0] == 'n':
                p_negative = Decimal(val[1])
            if val[0] == 't':
                p_truthful = Decimal(val[1])
            elif val[0] == 'd':
                p_deceptive = Decimal(val[1])

        for line in f:
            val = line.strip().split('=*=')
            prob = val[1].split('|')
            inner = {}
            for p in prob:
                t = p.split(':')
                inner[t[0]] = Decimal(t[1])
#                print(condProb)
            condProb[val[0]] = inner

p_positive = 0
p_negative = 0
p_truthful = 0
p_deceptive = 0
condProb = {}
setup()
#print(condProb)
wfile = open('nboutput.txt', 'w')
tokenizeClassify()
wfile.close()
