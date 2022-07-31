import re, json, ast, csv
import pandas as pd
import collections.abc
import os
import sys, getopt

inputtsv = None
outputtsv = None
langs = []

opts, args = getopt.getopt(sys.argv[1:], "i:o:l:", ["input = ", "output = ", "lang ="])
for opt, arg in opts:
    if opt in ['-i', '--input']:
        inputtsv = arg
    elif opt in ['-o', '--output']:
        outputtsv = arg
    elif opt in ['-l', '--lang']:
        langs = arg.split(',')

if outputtsv is None and inputtsv is not None:
    outputtsv = re.sub('\.tsv$', '.edited.tsv', inputtsv)

f1 = None
f2 = None
words = {}

print(inputtsv, outputtsv, langs)

try:
    f1 = open(inputtsv, "r")
    f2 = open(outputtsv, "w")
except:
    print ('Error: File handling')

try:
    words = json.load(open('new.json','r'))
except:
    print ('Error reading word JSON')

panels = []
tsv_reader = csv.reader(f1, delimiter='\t')
tsv_writer = csv.writer(f2, delimiter='\t') 
wordcount = 0
notfound = 0
for i, line in enumerate(tsv_reader):
    if i%4 == 0:
        panels = []
        panels.append(line)
    else:
        panels.append(line)
    if i%4 == 3:
        tsv_writer.writerow(panels[0])
        tsv_writer.writerow(panels[1])
        tsv_writer.writerow(panels[2])
        if (len(panels[1]) != len(panels[2]) or 
            len(panels[2]) != len(panels[3])
            ):
            print(f'Warning: Length mismatch {panels[0]}')
        gloss = []
        for j, word in enumerate(panels[1]):
            wordobjs = None
            try:
                if word != '':
                    wordcount += 1
                    wordobjs = words[word]
            except:
                print(f'Word not found: {word}')
                notfound += 1
            if wordobjs is None:
                gloss.append(panels[3][j])
            else:
                selected = wordobjs[0]
                if len(wordobjs) > 1 and selected['jp'] != panels[2][j]:
                    for wordobj in wordobjs[1:]:
                        if wordobj['jp'] == panels[2][j]:
                            selected = wordobj 
                gloss.append(panels[3][j] + '#' + '#'.join([selected[lang] for lang in langs]))    
        tsv_writer.writerow(gloss)

print (f'Handled {wordcount} words, {notfound} words not found')