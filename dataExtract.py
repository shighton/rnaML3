# Pull labels and sequences out of data pool

import re

with open('/Users/shighton/PycharmProjects/rnaML3/src/MHL_hsa_sep29_trnSet_miRNAgrpby_20_80.arff', 'r') as file:
    data = file.read()

missFile = open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedMisses.txt', 'w')
hitFile = open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedHits.txt', 'w')

labeled_misses = re.findall('0\\s%\\s\\w{22}&\\w{25}', data)
labeled_hits = re.findall('1\\s%\\s\\w{22}&\\w{25}', data)

misses = ''
hits = ''

for miss in labeled_misses:
    temp = re.search('\\w{22}&\\w{25}', miss)
    grouped = temp.group()
    for char in grouped:
        if char == 'A':
            grouped += '2'
        elif char == 'U':
            grouped += '3'
        elif char == 'G':
            grouped += '4'
        elif char == 'C':
            grouped += '5'
        elif char == 'Z':
            grouped += '6'
        elif char != '&':
            print("Nucleotide not recognized")

    temp = re.search('\\d{22}\\d{25}', grouped)
    digitized = temp.group()
    misses += digitized + "\n"

missFile.write(misses)
missFile.close()

for hit in labeled_hits:
    temp = re.search('\\w{22}&\\w{25}', hit)
    grouped = temp.group()
    for char in grouped:
        if char == 'A':
            grouped += '2'
        elif char == 'U':
            grouped += '3'
        elif char == 'G':
            grouped += '4'
        elif char == 'C':
            grouped += '5'
        elif char == 'Z':
            grouped += '6'
        elif char != '&':
            print("Nucleotide not recognized")

    temp = re.search('\\d{22}\\d{25}', grouped)
    digitized = temp.group()
    hits += digitized + "\n"

hitFile.write(hits)
hitFile.close()
