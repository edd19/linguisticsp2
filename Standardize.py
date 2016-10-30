#!/usr/bin/env python3
import string

ban = [',', '"', '-', ';', ':', '(', ')', '-', '_', '[', ']', '}', '{', '"']
endmark = ['.', '!', '?']
#LIMITE : les mots tels que "M." coupent la phrase en plein milieu

#line as input and returns a line with the corresponding markers and a standardized line
def process_line(line):
    yo = ''
    if line !='\n': #if one line is empty
        yo = yo +'<s> '

    for x in range(0, len(line)):
        if no_endmark(line) and line[x] == '\n':
            yo = yo + '</s>'
        elif line[x] not in ban and line[x] not in endmark: #keep adding characters
            yo=yo+line[x]
        elif line[x] not in ban and line[x] in endmark: #removes end of sentence and add markers
            yo = yo + ' </s> '
            yo = yo + '<s> '

    if (yo.count('<s>')!=1): #Removes extra starting markers
        yo = replace_right(yo, '<s>', '', 1)

    if (yo.count('</s>')!=1): #Removes extra ending markers
        yo = replace_right(yo, '</s>', '', 1)

    yo = yo.upper()
    return " ".join(yo.split()) #Removes extra space



#to remove the last occurence from the right
def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

def no_endmark(line):
    if '.' not in line or '!' not in line or '?' not in line:
        return True
    return False


#takes the text as input and returns a standardized text
def standardize(input):
    with open(input, 'r') as f:
        with open('output.txt', 'w') as f2:
            for line in f:
                #print(line, end='\n')
                newline = process_line(line)

                #print(newline, end='\n')
                f2.write(newline)
                f2.write('\n')
        f2.closed
    f.closed

dumas = 'Dumas/Dumas_train.txt' #ne marche pas à cause de la ligne 14144
test = 'test.txt'
#standardize(dumas)