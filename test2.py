import json
import os

file_name = os.path.join(os.path.abspath('activites.json'))

print(file_name)

js_file = json.load(open(file_name))

for majorkey, subdict in js_file.items():
    # print (majorkey)
    print(subdict)    
    # for subkey, value in subdict.items():
        # print(subkey)
        # print(value)
    
