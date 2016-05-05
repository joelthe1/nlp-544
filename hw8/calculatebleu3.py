import codecs
import os
import sys
import functools
from math import exp, log

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

def ngramize_and_count(sentence, n=1):
    sentence = sentence.lower()
    tokens = sentence.strip().split()
    ngrams = []
    for x in range(len(tokens)-n+1):
        ngrams.append(' '.join(tokens[x:n+x]))
    return count(ngrams)

def readin(path, ref=0):
    if os.path.isdir(path):
        refs = []
        for root, sdirs, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(root, filename)
                refs.append(openup(file_path))
        return refs
    else:
        if ref == 1:
            return [openup(path)]
        return openup(path)

def mod_precision_counts(candidate_data, ref_data, n):
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
        if candidate_counts:
            denom += functools.reduce(lambda x,y:x+y, candidate_counts.values())
        else:
            denom += 1
        cand_len = len(sentence.strip().split())
        c += cand_len
        temp_r = float('inf')
        for refs in ref_data:
            l = len(refs[index].strip().split())
            if abs(temp_r-cand_len) > abs(l-cand_len):
                temp_r = l
            ref_counts.append(ngramize_and_count(refs[index], n))
        r += temp_r
        for ngram in candidate_counts.keys():
            cand_count = candidate_counts[ngram]
            val = 0
            for ref in ref_counts:
                if ngram in ref:
                    if val < ref[ngram]:
                        val = ref[ngram]
            clipped_count = min(cand_count, val)
            sentence_sum += clipped_count
        numerator += sentence_sum
    if numerator == 0 or denom == 0:
        return (r, c, 0)
    return (r, c, numerator/denom)

if __name__ == '__main__':
    ref_data = readin(ref_path, 1)
    candidate_data = readin(candidate_path)
    mod_p_values = []

    # N in the paper.
    N = 4

    for n in range(1, N+1):
        mod_p_values.append(mod_precision_counts(candidate_data, ref_data, n))

    r,c = mod_p_values[0][0], mod_p_values[0][1]

    bp = 1.0-(r/c)
    
    gavg = 0
    # Geometric avg. of Pn
    for p in mod_p_values:
        gavg += log(p[2])
    logbleu = min(bp, 0) + gavg/N
    bleu = exp(logbleu)
#    print('BLUE score is', bleu)
    with open('bleu_out.txt', 'w',) as wfile:
        wfile.write(str(bleu))
