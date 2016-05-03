import codecs
import os
import sys

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
    tokens = sentence.split(' ')
    ngrams = []
    for x in range(len(tokens)-n+1):
        ngrams.append(' '.join(tokens[x:n+x]))
    return count(ngrams)

#def compare(cand, refs):

def readin(path):
    if os.path.isdir(path):
        refs = []
        for root, sdirs, files in os.walk(path):
            for filename in files:
                print(filename)
                file_path = os.path.join(root, filename)
                refs.append(openup(file_path))
        return refs
    else:
        print(path)
        return openup(path)

if __name__ == '__main__':
    ref_data = readin(ref_path)
    print(len(ref_data))
    candidate_data = readin(candidate_path)
    print(len(candidate_data))

    for index, sentence in enumerate(candidate_data):
        if sentence == '':
            continue
        candidate_counts = ngramize_and_count(sentence)
        exit()
