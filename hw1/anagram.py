import sys

if len(sys.argv) < 2:
    print "No input text given."
    exit()

def permute(text, res=''):
    if len(text) == 1:
        result.append(res+text)
    for x in text:
        text_copy = text.replace(x, '')
        permute(text_copy, res+x)

result = []
wfile = open('anagram_out.txt', 'w')
permute(sys.argv[1])
output = sorted(result, key=str.lower)

for r in output:
    wfile.write(r + '\n')
wfile.close()
