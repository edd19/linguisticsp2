#!/usr/bin/env python3
import string

ban = [',', '"', '-', ';', ':', '(', ')', '-', '_', '[', ']', '}', '{', '"']
endmark = ['\n','.', '!', '?']
#LIMITE : les mots tels que "M." coupent la phrase en plein milieu


#TODO Les lignes où il n'y a pas de ponctuation ne reçoivent pas de marqueurs : pas réussi à traiter le cas où line[x] == '\n'
#TODO la lecture du fichier s'arrête à la ligne 14144, cette ligne ne peut pas être lue, le reste est ok


#line as input and returns a line with the corresponding markers and a standardized line
def process_line(line):
    yo = ''
    if line !='\n': #if one line is empty
        yo = yo +'<s> '

    for x in range(0, len(line)):
        if line[x] not in ban and line[x] not in endmark: #keep adding characters
            yo=yo+line[x]
        elif line[x] not in ban and line[x] in endmark: #removes end of sentence and add markers
            yo = yo + ' </s> '
            yo = yo + '<s> '

    if (yo.count('<s>')!=1): #pour eviter de retirer le marker unique en début de ligne
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
                print(line, end='\n')
                newline = process_line(line)

                print(newline, end='\n')
                f2.write(newline)
                f2.write("\n")
        f2.closed
    f.closed

dumas = '/home/ndizera/Documents/MA2/Q1/LINGI2263-Computational_Linguistics/Mission/Dumas/Dumas_train.txt' #ne marche pas à cause de la ligne 14144
dumas2 = 'Dumas/Dumas_train2.txt' #sans la ligne 14144 ca marche
test = 'test.txt'
standardize(dumas)