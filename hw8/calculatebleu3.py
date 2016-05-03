import codecs
import os
import sys
import functools
from decimal import *

# check for arguments
if len(sys.argv) < 3:
    print('Error! Not enough arguments.')
    exit()

candidate_path = sys.argv[1]
ref_path = sys.argv[2]

# check path existence
if not os.path.exists(candidate_path) or not os.path.exists(ref_path):
    print('Error! Given path(s) is not a valid directory.')
    exit()

def count(ngrams):
    counts = {}
    for ng in ngrams:
        if ng not in counts:
            counts[ng] = 1
        else:
            counts[ng] += 1
    return counts

def openup(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        data = f.read().split('\n')
        return data
#        ngrams = ngramize(data[2].strip())
#        count(ngrams)

def ngramize_and_count(sentence, n=1):
    tokens = sentence.strip().split(' ')
    ngrams = []
    for x in range(len(tokens)-n+1):
        ngrams.append(' '.join(tokens[x:n+x]))
    return count(ngrams)

def readin(path, ref=0):
    if os.path.isdir(path):
        refs = []
        for root, sdirs, files in os.walk(path):
            for filename in files:
                print(filename)
                file_path = os.path.join(root, filename)
                refs.append(openup(file_path))
        return refs
    else:
        if ref == 1:
            return [openup(path)]
        print(path)
        return openup(path)

def len_diff(candidate_sentence, ref_sentence):
    pass

def mod_precision(candidate_data, ref_data, n):
    numerator = 0
    denom = 0
    r, c = 0, 0
    for index, sentence in enumerate(candidate_data):
        if sentence == '':
            continue
        matches = {}
        ref_counts = []
        sentence_sum = 0
        candidate_counts = ngramize_and_count(sentence, n)
        denom += functools.reduce(lambda x,y:x+y, candidate_counts.values())
        c += len(sentence.strip().split(' '))
        temp_r = float('inf')
        for refs in ref_data:
            l = len(refs[index].strip().split(' '))
            if temp_r > abs(l-c):
                temp_r = l
            ref_counts.append(ngramize_and_count(refs[index], n))
        r += temp_r
        for ngram in candidate_counts:
            val = 0
            for ref in ref_counts:
                if ngram in ref:
                    if val < ref[ngram]:
                        val = ref[ngram]
            sentence_sum += val
        numerator += sentence_sum
    return (r, c, Decimal(numerator/denom))

if __name__ == '__main__':
    ref_data = readin(ref_path, 1)
    print(len(ref_data))
    candidate_data = readin(candidate_path)
    print(len(candidate_data))
    mod_p_values = []

    # N in the paper.
    N = 2

    for n in range(1, N+1):
        mod_p_values.append(mod_precision(candidate_data, ref_data, n))
    print(mod_p_values)

    r,c = Decimal(mod_p_values[0][0]), Decimal(mod_p_values[0][1])

    # Calculate BP
    bp = None
    if c > r:
        bp = Decimal(1)
    else:
        bp = Decimal(1-(r/c)).exp()
    
    print(bp)

    gavg = 0
    # Geometric avg. of Pn
    for n,p in enumerate(mod_p_values):
        gavg += Decimal(Decimal(p[2]).ln()/(n+1))
    print(gavg)
    exp_gavg = gavg.exp()

    blue = Decimal(bp*exp_gavg)
    print('BLUE score is %d' % blue)