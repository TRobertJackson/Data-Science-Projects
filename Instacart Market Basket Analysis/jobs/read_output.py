import glob
import pandas as pd
import numpy as np
import pickle


list_of_files = glob.glob('./*.txt')
list_of_empty_files = []
cols  = ['learning_rate', 'max_depth', 'n_estimators', 'gamma', 'min_child_weight', 'subsample', 'max_score', 'opt_threshold']

output = pd.DataFrame(columns = cols)

for filename in list_of_files:
    result = open(filename, "r").readlines()
    if len(result) == 0:
        list_of_empty_files.append(filename)
    else:
        result = result[0].replace('(', '').replace(')','').replace(',','').split()
        if len(result) == 0:
            list_of_empty_files.append(filename)
            continue
        result = pd.DataFrame([result], columns = cols)
        output = output.append(result)

output = output.apply(pd.to_numeric)
output.sort_values('max_score', ascending = False, inplace = True)
print(list_of_empty_files)
print(output)
pickle.dump(output, open('output.p', 'wb'))
pickle.dump(list_of_empty_files, open('list_of_empty_files.p', 'wb'))
