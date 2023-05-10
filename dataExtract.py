# Pull labels and sequences out of data pool
# Concatenate and digitize nucleotide sequences
# Write finished digitized sequences to respective files
# Extract free energies and number of bonds
# Write to separate files for passing to model.py

import re

with open('/Users/shighton/PycharmProjects/rnaML3/src/MHL_hsa_sep29_trnSet_miRNAgrpby_20_80.arff', 'r') as file:
    data = file.read()

missFile = open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedMisses.txt', 'w')
hitFile = open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedHits.txt', 'w')
numMissBondsFile = open('/Users/shighton/PycharmProjects/rnaML3/src/numMissBonds.txt', 'w')
numHitBondsFile = open('/Users/shighton/PycharmProjects/rnaML3/src/numHitBonds.txt', 'w')
energyMissFile = open('/Users/shighton/PycharmProjects/rnaML3/src/missFreeEnergy.txt', 'w')
energyHitFile = open('/Users/shighton/PycharmProjects/rnaML3/src/hitFreeEnergy.txt', 'w')

labeled_misses = re.findall('0\\s%\\s\\w{22}&\\w{25}\\s\\W{22}&\\W{25}\\s[0|-]?\\d+.\\d+', data)
labeled_hits = re.findall('1\\s%\\s\\w{22}&\\w{25}\\s\\W{22}&\\W{25}\\s[0|-]?\\d+.\\d+', data)

misses = ''
hits = ''
bondCount = 0
energy = ''

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

for miss in labeled_misses:
    temp = re.search('\\W{22}', miss)
    grouped = temp.group()
    for char in grouped:
        if char == '(':
            bondCount += 1

    numMissBondsFile.write(str(bondCount) + '\n')
    bondCount = 0
numMissBondsFile.close()

for miss in labeled_misses:
    temp = re.search('[0|-]?\\d+.\\d+', miss)
    grouped = temp.group()
    energy += grouped + '\n'

energyMissFile.write(energy)
energyMissFile.close()

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

for hit in labeled_hits:
    temp = re.search('\\W{22}', hit)
    grouped = temp.group()
    for char in grouped:
        if char == '(':
            bondCount += 1

    numHitBondsFile.write(str(bondCount) + '\n')
    bondCount = 0
numHitBondsFile.close()

energy = ''

for hit in labeled_hits:
    temp = re.search('[0|-]?\\d+.\\d+', hit)
    grouped = temp.group()
    energy += grouped + '\n'

energyHitFile.write(energy)
energyHitFile.close()
