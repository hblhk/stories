import csv
import pandas as pd

storylist = pd.read_csv('storylist.csv')
storylist.fillna('', inplace=True)

inputpath = '../sheets/'

for i, row in storylist.iterrows():
    storyid = row['storyid']
    inputtsv = row['legacysheet']
    if inputtsv != '': 
        try:
            with open(inputpath + inputtsv, encoding="UTF-8") as f:
                print(f'StoryID {storyid}')
                j = 0
                clsmax = 0
                clserr = 0
                errrow = []
                for line in f:
                    j += 1
                    #print(line, end='')
                    cls1 = line.count(',')
                    cls2 = line.count(', ')
                    cls = cls1 - cls2
                    #print(f'Columns in Row {j} : {cls} - {cls2} = {cls}')
                    
                    if cls != clsmax:
                        if j > 1:
                            clserr = 1
                            errrow.append(j)
                            print(f'COLERR: Columns in Row {j} : {cls1} - {cls2} = {cls}, Expected {clsmax}')
                            
                        if cls > clsmax:
                            clsmax = cls
                    
                print(f'Total Number of Rows: {j}; Max Columns: {clsmax}')

                if j%4 != 0:
                    print(f'ROW ERROR DETECTED')
                else:
                    print(f'Row OK')
                
                if clserr > 0:
                    print(f'COLUMN ERROR DETECTED: SEE ABOVE')
                else:
                    print(f'Column OK')
                print(' ')
                #ad1 = f.readlines()
                #print (ad1)
        except:
            print (f'Error: File handling: {storyid} at {inputtsv}')
            continue       



