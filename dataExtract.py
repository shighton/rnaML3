# Pull labels and sequences out of data pool

import re

with open('/Users/shighton/PycharmProjects/rnaML3/src/MHL_hsa_sep29_trnSet_miRNAgrpby_20_80.arff', 'r') as file:
    data = file.read()

misses = re.search('0\\s\\%\\s\\w{22}\\&\\w{25}', data)

misses.group()