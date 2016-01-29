import os
import sys
from os.path import join

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

def tokenize():
    N_positive = 0
    N_negative = 0
    N_truthful = 0
    N_deceptive = 0
    N = 0
    for root, sdirs, files in os.walk(path):
#        print('root = ' + root)
#            print('\t- file %s (full path: %s)' % (filename, file_path))
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.startswith('.') or 'fold' not in file_path:
                continue
            N += 1
            words = file_teardown(file_path)
            if 'positive_' in root and 'truthful_' in root:
                N_positive += 1
                N_truthful += 1
                update_helper(words, positive, truthful)
            elif 'positive_' in root and 'deceptive_' in root:
                N_positive += 1
                N_deceptive += 1
                update_helper(words, positive, deceptive)
            elif 'negative_' in root and 'truthful_' in root:
                N_negative += 1
                N_truthful += 1
                update_helper(words, negative, truthful)
            elif 'negative_' in root and 'deceptive_' in root:
                N_negative += 1
                N_deceptive += 1
                update_helper(words, negative, deceptive)
    print(N_positive)
    print(N_negative)
    print(N_truthful)
    print(N_deceptive)
    print(N)

def update_helper(words, category1, category2):
    global vocab_count
    for word in words:
        if word in exceptions:
            continue
        vocab_count += 1
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
vocab_count = 0
exceptions = ['','a','about','above','after','again','against','all','am','an','and','any','are','aren\'t','as','at','be','because','been','before','being','below','between','both','but','by','can\'t','cannot','could','couldn\'t','did','didn\'t','do','does','doesn\'t','doing','don\'t','down','during','each','few','for','from','further','had','hadn\'t','has','hasn\'t','have','haven\'t','having','he','he\'d','he\'ll','he\'s','her','here','here\'s','hers','herself','him','himself','his','how','how\'s','i','i\'d','i\'ll','i\'m','i\'ve','if','in','into','is','isn\'t','it','it\'s','its','itself','let\'s','me','more','most','mustn\'t','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours,ourselves','out','over','own','same','shan\'t','she','she\'d','she\'ll','she\'s','should','shouldn\'t','so','some','such','than','that','that\'s','the','their','theirs','them','themselves','then','there','there\'s','these','they','they\'d','they\'ll','they\'re','they\'ve','this','those','through','to','too','under','until','up','very','was','wasn\'t','we','we\'d','we\'ll','we\'re','we\'ve','were','weren\'t','what','what\'s','when','when\'s','where','where\'s','which','while','who','who\'s','whom','why','why\'s','with','won\'t','would','wouldn\'t','you','you\'d','you\'ll','you\'re','you\'ve','your','yours','yourself','yourselves']

tokenize()

print(vocab_count)
