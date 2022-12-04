import csv
import pandas as pd

storylist = pd.read_csv('storylist.csv')
storylist.fillna('', inplace=True)

inputpath = '../sheets/'

for i, row in storylist.iterrows():
    storyid = row['storyid'] # consider adopt single storyid for all filenames i.e. XML, PDF, etc.
    inputtsv = row['legacysheet'] # may not be legacy afterall lol
    if inputtsv != '': 
        try:
            with open(inputpath + inputtsv, encoding="UTF-8") as f:
                print(f'StoryID {storyid}')
                j = 0 # set and reset counter for each story
                clsexp = 0
                clsmax = 0
                rerr = 0 # flag for row error

                for line in f:
                    j += 1
                    #print(line, end='') # extra debug lines
                    cls1 = line.count(',')
                    cls2 = line.count(', ') #also catch extra whitespace as bonus
                    cls = cls1 - cls2 #actually number of commas but more useful for fix anyways
                    #print(f'Columns in Row {j} : {cls} - {cls2} = {cls}') # extra debug lines
                    
                    # Row Checks for each Row
                    match j%4:
                        case 1:
                            if line.count('[') != 1:
                                print(f'ROWERR: Row {j} : Format error in Panel Row 1 (Incorrect Number of [ )')
                            if line.count(']') != 1:
                                print(f'ROWERR: Row {j} : Format error in Panel Row 1 (Incorrect Number of ] )')
                        case 2:
                            pass
                            #if line.count('x') != 1: # placeholder check for (any) valid Cantonese sentence?
                            #    print(f'ROWERR: Row {j} : Format error in Panel Row 2 (???)')
                        case 3:
                            hash3 = line.count('#')
                            if hash3 < 0:
                                print(f'ROWERR: Row {j} : Unexpected Format in Panel Row 3 (Missing #)')
                        case 0:
                            hash4 = line.count('#')
                            if hash4 < 0:
                                print(f'ROWERR: Row {j} : Unexpected Format in Panel Row 4 (Missing #)')
                            if hash3 != hash4:
                                print(f'ROWERR: Row {j} : Unexpected Format in Panel Row 3/4 (# Mismatch: {hash3} to {hash4})')
                    
                    # Column Checks in each Row
                    if cls != clsexp:
                        if cls > clsmax:
                            clsmax = cls
                        
                        if j == 1:
                            clsexp = cls #Row 1 should have correct number of cols
                        else:
                            if rerr == 0: # wonder if check is faster than assignment lol
                                rerr = 1
                            print(f'COLERR: Row {j} : Number of Column: {cls1} - {cls2} = {cls}, Expected {clsexp}')
                    
                # Looped through all rows
                print(f'Total Number of Rows: {j}; Maximum Columns: {clsmax}')

                if j%4 > 0:
                    print(f'ROW ERROR DETECTED: in TOTAL NUMBER OF ROW')
                else:
                    print(f'Row Number OK')
                
                if rerr > 0:
                    print(f'COLUMN ERROR DETECTED: SEE LOG ABOVE')
                else:
                    print(f'Column Number OK')
                
                print(' ') # line break for readability
                
                #ad1 = f.readlines()
                #print (ad1) # print all lines for debug
        except:
            print (f'Error: File handling: {storyid} at {inputtsv}')
            continue       



