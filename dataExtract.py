# Pull labels and sequences out of data pool

import re

with open('/Users/shighton/PycharmProjects/rnaML3/src/MHL_hsa_sep29_trnSet_miRNAgrpby_20_80.arff', 'r') as file:
    data = file.read()

labeled_misses = re.findall('0\\s%\\s\\w{22}&\\w{25}', data)

labeled_hits = re.findall('1\\s%\\s\\w{22}&\\w{25}', data)

misses = ''
hits = ''

for miss in labeled_misses:
    temp = re.search('\\w{22}&\\w{25}', miss)
    misses += temp.group() + "\n"

for hit in labeled_hits:
    temp = re.search('\\w{22}&\\w{25}', hit)
    hits += temp.group() + "\n"

print(hits)
