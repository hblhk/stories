from xml.dom import minidom
import os 
import re, json, ast, csv
import collections.abc
import sys, getopt
import pandas as pd

root = minidom.Document()

storylist = pd.read_csv('storylist.csv')
storylist.fillna('', inplace=True)

inputpath = '../sheets/'
outputpath = '../tmp/'

def GenerateWord (char, jyutping, gloss):
    w = root.createElement('w')
    pc = root.createElement('pc')
    if jyutping != '#' and gloss != '#':
        w.appendChild(root.createTextNode(char))
        w.setAttribute('lemma', jyutping)
        w.setAttribute('msd', gloss)
        return w
    else:
        pc.appendChild(root.createTextNode(char))
        return pc

def GenerateSentence(panels):
    l = root.createElement('l') 
    if (len(panels[1]) != len(panels[2]) or 
        len(panels[2]) != len(panels[3])
        ):
        print(f'Warning: Length mismatch {panels[0]}: {len(panels[1])},{len(panels[2])},{len(panels[3])}')
        print(panels[1])
    for j, word in enumerate(panels[1]):
        if word != '':
            l.appendChild(GenerateWord(panels[1][j], panels[2][j], panels[3][j]))
    return l

def GenerateStoryText(tsv_reader):
    panels = []
    text = root.createElement('text')
    body = root.createElement('body')
    text.appendChild(body)
    for i, line in enumerate(tsv_reader):
        if i%4 == 0:
            panels = []
            panels.append(line)
        else:
            panels.append(line)
        if i%4 == 3:
            body.appendChild(GenerateSentence(panels))
    return text

def GenerateStoryHeader(row):
    teiHeader = root.createElement('teiHeader')
    fileDesc = root.createElement('fileDesc')

    titleStmt = root.createElement('titleStmt')

    title = root.createElement('title')
    title.appendChild(root.createTextNode(row['titleC']))
    titleStmt.appendChild(title)

    author = root.createElement('author')
    author.appendChild(root.createTextNode(row['author']))
    titleStmt.appendChild(author)

    if (row['editor']):
        editor = root.createElement('editor')
        editor.appendChild(root.createTextNode(row['editor']))
        titleStmt.appendChild(editor)

    respStmt = root.createElement('respStmt')

    if row['cantoneseTeam']:
        resp = root.createElement('resp')
        resp.appendChild(root.createTextNode('Cantonese Team'))
        persName = root.createElement('persName')
        persName.appendChild(root.createTextNode(row['cantoneseTeam']))
        respStmt.appendChild(resp)
        respStmt.appendChild(persName)

    if row['originalAuthor']:
        resp = root.createElement('resp')
        resp.appendChild(root.createTextNode('Original Author'))
        persName = root.createElement('persName')
        persName.appendChild(root.createTextNode(row['originalAuthor']))
        respStmt.appendChild(resp)
        respStmt.appendChild(persName)

    if respStmt.childNodes:
        titleStmt.appendChild(respStmt)

    publicationStmt = root.createElement('publicationStmt')
    publisher = root.createElement('publisher')
    publisher.appendChild(root.createTextNode('Hambaanglaang'))

    pubPlace = root.createElement('pubPlace')
    pubPlace.appendChild(root.createTextNode('Hong Kong'))

    date = root.createElement('date')
    date.appendChild(root.createTextNode('2022'))

    idno1 = root.createElement('idno')

    availability = root.createElement('availability')
    availability.setAttribute('status','restricted')

    licence = root.createElement('licence')
    licence.setAttribute('target','http://creativecommons.org/licenses/by/4.0/')
    licence.appendChild(root.createTextNode('Attribution 4.0 International (CC BY 4.0)'))

    availability.appendChild(licence)

    publicationStmt.appendChild(publisher)
    publicationStmt.appendChild(pubPlace)
    publicationStmt.appendChild(date)
    publicationStmt.appendChild(idno1)
    publicationStmt.appendChild(availability)

    seriesStmt = root.createElement('seriesStmt')
    title2 = root.createElement('title')
    title2.appendChild(root.createTextNode('Hambaanglaang Graded Readers 冚唪唥粵文讀本'))
    idno2 = root.createElement('idno')
    idno2.appendChild(root.createTextNode(storyid))
    seriesStmt.appendChild(title2)
    seriesStmt.appendChild(idno2)

    sourceDesc = root.createElement('sourceDesc')

    if row['attribution']:
        nodeP = root.createElement('p')
        nodeP.appendChild(root.createTextNode(row['attribution']))
        sourceDesc.appendChild(nodeP)

    fileDesc.appendChild(titleStmt)
    fileDesc.appendChild(publicationStmt)
    fileDesc.appendChild(seriesStmt)
    fileDesc.appendChild(sourceDesc)

    teiHeader.appendChild(fileDesc)

    return teiHeader

def GenerateStory(row, tsv_reader):
    nodeTEI = root.createElement('TEI')
    nodeTEI.setAttribute('xmlns', 'http://www.tei-c.org/ns/1.0')
    nodeTEI.appendChild(GenerateStoryHeader(row))
    nodeTEI.appendChild(GenerateStoryText(tsv_reader))
    return nodeTEI

def GenerateCorpusHeader():
    header = root.createElement('teiHeader')
    return header

def GenerateCorpus():
    teiCorpus = root.createElement('teiCorpus')
    teiCorpus.setAttribute('version','3.3.0')
    teiCorpus.setAttribute('xmlns','http://www.tei-c.org/ns/1.0')
    teiCorpus.appendChild(GenerateCorpusHeader())
    return teiCorpus

# inputtsv = None
# outputxml = None
# opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input = ", "output = "])
# for opt, arg in opts:
#     if opt in ['-i', '--input']:
#         inputtsv = arg
#     elif opt in ['-o', '--output']:
#         outputxml = arg

# if outputxml is None and inputtsv is not None:
#     outputxml = re.sub('\.tsv$', '.xml', inputtsv)

for i, row in storylist.iterrows():
    storyid = row['storyid']
    inputtsv = row['legacysheet']
    if inputtsv != '':
        f1 = None
        f2 = None
        
        try:
            f1 = open(inputpath + inputtsv, "r", encoding="utf-8")
            f2 = open(f'{outputpath}{storyid}.xml', "w", encoding="utf-8")
        except:
            print (f'Error: File handling: {row}')
            continue        
        tsv_reader = csv.reader(f1)
        xml_str = GenerateStory(row, tsv_reader).toprettyxml(indent ="\t")
        f2.write(xml_str)
        f2.close()


