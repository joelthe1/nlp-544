import re

def separate(token):
    patt = re.compile(r'(.*)\/([A-Z0-9]{2})')
    res = patt.match(token)
    #TODO: if res: for safety
    word = res.group(1)
    tag = res.group(2)
    return {'word': word, 'tag': tag}

total_tags = 0
corr_tags = 0
with open('hmmoutput.txt', 'r') as rfile, open('hw6-dev-train/dev/catalan_corpus_dev_tagged.txt', 'r') as rubericfile:
    for inp_line in rfile.readlines():
        ruberic_line = rubericfile.readline()

        inp_line_split = inp_line.strip().split(' ')
        ruberic_line_split = ruberic_line.strip().split(' ')
        total_tags += len(ruberic_line_split)
        for index, inp_token in enumerate(inp_line_split):
            inp = separate(inp_token)
            rub = separate(ruberic_line_split[index])
            if inp['word'] != rub['word']:
                print('Word mismatch. Errored out.')
                exit()
            if inp['tag'] == rub['tag']:
                corr_tags += 1

print('Accuracy is:', corr_tags/total_tags)
