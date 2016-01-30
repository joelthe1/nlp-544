import os
import sys
from os.path import join
from decimal import *

path = sys.argv[1]
if not os.path.exists(path):
    print('Error! Given path is not a valid directory.')
    exit()

def tokenize():
    global N_positive, N_negative, N_truthful, N_deceptive, N
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

def update_helper(words, category1, category2):
    for word in words:
        if word in exceptions:
            continue
        if word in vocabulary:
            vocabulary[word] += 1
        else:
            vocabulary[word] = 1
        
        if word in category1:
            category1[word] += 1
        else:
            category1[word] = 1

        if word in category2:
            category2[word] += 1
        else:
            category2[word] = 1

def file_teardown(file_path):
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'
    with open(file_path) as f:
        return map(lambda w: w.lower().strip(punct), f.read().split())

def calc_p(word):
    Tct = 1
    if word in positive:
        Tct += positive[word]
    pdc = Decimal(Tct)/(Decimal(T_positive)+Decimal(vocab_count))
    wfile.write('p:'+str(pdc)+'|')
    
    Tct = 1
    if word in negative:
        Tct += negative[word]
    pdc = Decimal(Tct)/(Decimal(T_negative)+Decimal(vocab_count))
    wfile.write('n:'+str(pdc)+'|')

    Tct = 1
    if word in truthful:
        Tct += truthful[word]
    pdc = Decimal(Tct)/(Decimal(T_truthful)+Decimal(vocab_count))
    wfile.write('t:'+str(pdc)+'|')
    
    Tct = 1
    if word in deceptive:
        Tct += deceptive[word]
    pdc = Decimal(Tct)/(Decimal(T_deceptive)+Decimal(vocab_count))
    wfile.write('d:'+str(pdc)+'\n')

def write_p():
    #Write prior Ps
    t = Decimal(N_positive)/Decimal(N)
    wfile.write('p:'+str(t)+'|')
    
    t = Decimal(N_negative)/Decimal(N)
    wfile.write('n:'+str(t)+'|')
    
    t = Decimal(N_truthful)/Decimal(N)
    wfile.write('t:'+str(t)+'|')

    t = Decimal(N_deceptive)/Decimal(N)
    wfile.write('d:'+str(t)+'\n')

    for word in vocabulary:
        wfile.write(word+'=*=')
        calc_p(word)

N_positive = 0
N_negative = 0
N_truthful = 0
N_deceptive = 0
N = 0

positive = {}
negative = {}
truthful = {}
deceptive = {}
vocabulary = {}

#exceptions = []
exceptions = ['','a','about','above','after','again','against','all','am','an','and','any','are','aren\'t','as','at','be','because','been','before','being','below','between','both','but','by','can\'t','cannot','could','couldn\'t','did','didn\'t','do','does','doesn\'t','doing','don\'t','down','during','each','few','for','from','further','had','hadn\'t','has','hasn\'t','have','haven\'t','having','he','he\'d','he\'ll','he\'s','her','here','here\'s','hers','herself','him','himself','his','how','how\'s','i','i\'d','i\'ll','i\'m','i\'ve','if','in','into','is','isn\'t','it','it\'s','its','itself','let\'s','me','more','most','mustn\'t','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours,ourselves','out','over','own','same','shan\'t','she','she\'d','she\'ll','she\'s','should','shouldn\'t','so','some','such','than','that','that\'s','the','their','theirs','them','themselves','then','there','there\'s','these','they','they\'d','they\'ll','they\'re','they\'ve','this','those','through','to','too','under','until','up','very','was','wasn\'t','we','we\'d','we\'ll','we\'re','we\'ve','were','weren\'t','what','what\'s','when','when\'s','where','where\'s','which','while','who','who\'s','whom','why','why\'s','with','won\'t','would','wouldn\'t','you','you\'d','you\'ll','you\'re','you\'ve','your','yours','yourself','yourselves']

tokenize()

#positive = pickle.load( open( "save_p.p", "rb" ) )
#negative = pickle.load( open( "save_n.p", "rb" ) )
#truthful = pickle.load( open( "save_t.p", "rb" ) )
#deceptive = pickle.load( open( "save_d.p", "rb" ) )
#vocabulary = pickle.load( open( "save_v.p", "rb" ) )

vocab_count = len(vocabulary)
T_positive = sum(positive.values())
T_negative = sum(negative.values())
T_truthful = sum(truthful.values())
T_deceptive = sum(deceptive.values())

#N_positive = 640
#N_negative = 640
#N_truthful = 640
#N_deceptive = 640
#N = 1280

#print(N_positive)
#print(N_negative)
#print(N_truthful)
#print(N_deceptive)
#print(N)
#print(vocab_count)

wfile = open('nbmodel.txt', 'w')
write_p()
wfile.close()

