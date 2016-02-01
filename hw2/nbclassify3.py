from decimal import Decimal
import sys
import os
from math import log

path = sys.argv[1]
def file_teardown(file_path):
    punct = '"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'
    with open(file_path) as f:
        return map(lambda w: w.lower().strip(punct), f.read().split())

def tokenizeClassify():
    global N
    for root, sdirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.startswith('.') or 'fold' not in file_path:
                continue
            N += 1
            words = file_teardown(file_path)
            classify(words, file_path)

def classify(words, file_path):
    global corr, tp, fp, tn, fn
    score = {}
    flag = 0
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
        if 'truthful' in file_path:
            flag += 1
            tp[0] += 1
        else:
            fp[0] += 1
    else:
        wfile.write('deceptive ')
        if 'deceptive' in file_path:
            flag += 1
            tn[0] += 1
        else:
            fn[0] += 1
        
    if score['p'] > score['n']:
        wfile.write('positive ')
        if 'positive' in file_path:
            flag += 1
            tp[1] += 1
        else:
            fp[1] += 1
    else:
        wfile.write('negative ')
        if 'negative' in file_path:
            flag += 1
            tn[1] += 1
        else:
            fn[1] += 1

    wfile.write(file_path + '\n')
    if flag == 2:
        corr += 1

def setup():
    global p_positive, p_negative, p_truthful, p_deceptive
    with open('nbmodel.txt', 'r') as f:
        priors = f.readline().strip().split('|')
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

corr = 0
N = 0

tp = [0, 0]
fp = [0, 0]
tn = [0, 0]
fn = [0, 0]

wfile = open('nboutput.txt', 'w')
tokenizeClassify()
wfile.close()
print(path)
print('Accuracy:', (corr*100)/N)
precision = [0, 0]
recall = [0, 0]
f1 = []

precision[0] = Decimal(tp[0])/(Decimal(tp[0]) + Decimal(fp[0]))
recall[0] = Decimal(tp[0])/(Decimal(tp[0]) + Decimal(fn[0]))
f1.append((Decimal(2)*precision[0]*recall[0])/(precision[0]+recall[0]))

precision[1] = Decimal(tp[1])/(Decimal(tp[1]) + Decimal(fp[1]))
recall[1] = Decimal(tp[1])/(Decimal(tp[1]) + Decimal(fn[1]))
f1.append((Decimal(2)*precision[1]*recall[1])/(precision[1]+recall[1]))

print('t/d f1 is:', f1[0])
print('p/n f1 is:', f1[1], '\n')
