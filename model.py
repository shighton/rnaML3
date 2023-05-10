# Read processed data files
# Put data in pandas DataFrames
# Plot data using matplotlib

import matplotlib.pyplot as plt
import pandas as pd

with open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedMisses.txt', 'r') as file1:
    missData = file1.read()

with open('/Users/shighton/PycharmProjects/rnaML3/src/digitizedHits.txt', 'r') as file2:
    hitData = file2.read()

with open('/Users/shighton/PycharmProjects/rnaML3/src/numMissBonds.txt', 'r') as file3:
    missBondData = file3.read()

with open('/Users/shighton/PycharmProjects/rnaML3/src/numHitBonds.txt', 'r') as file4:
    hitBondData = file4.read()

with open('/Users/shighton/PycharmProjects/rnaML3/src/missFreeEnergy.txt', 'r') as file5:
    missEnergyData = file5.read()

with open('/Users/shighton/PycharmProjects/rnaML3/src/hitFreeEnergy.txt', 'r') as file6:
    hitEnergyData = file6.read()

missList = []
hitList = []

for line in missData:
    missList.append(0)

for line in hitData:
    hitList.append(1)

missDF = pd.DataFrame(list(zip(missList, missData.split(), missBondData.split(), missEnergyData.split())), columns=['Label', 'Sequence', 'NumBonds', 'Energy'])

hitDF = pd.DataFrame(list(zip(hitList, hitData.split(), hitBondData.split(), hitEnergyData.split())), columns=['Label', 'Sequence', 'NumBonds', 'Energy'])

frames = [missDF, hitDF]

result = pd.concat(frames)

#print(missDF.head(), '\n\n', hitDF.head())

#print(result.head())

plt.scatter(result['NumBonds'], result['Sequence'])
plt.show()
