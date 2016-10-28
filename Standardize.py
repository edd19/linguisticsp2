#!/usr/bin/env python3
import string

ban = [',', '"', '-', ';', ':', '(', ')', '-', '_']
endmark = ['.', '!', '?', '\n']


#line as input and returns a line with the corresponding markers and a standardized line
def process_line(line):
    yo = ''
    yo = yo +'<s> '

    for x in range(0, len(line)-1):
        if line[x] not in ban and line[x] not in endmark:
            yo=yo+str(line[x])
        elif line[x] not in ban and line[x] in endmark:
            yo = yo + ' </s> '
            yo = yo + '<s> '
    yo = replace_right(yo, '<s>', '', 1)
    return yo.upper()

#to remove the last occurence from the right
def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

#takes the text as input and returns a standardized text
def standardize(input):
    with open(input, 'r') as f:
        with open('output.txt', 'w') as f2:
            for line in f:
                #print(line, end='\n')
                newline = process_line(line)

                #print(newline, end='\n')
                f2.write(newline)
                f2.write("\n")
        f2.closed
    f.closed

dumas = 'Dumas/Dumas_train.txt'
test = 'test.txt'
#standardize(dumas)