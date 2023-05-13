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

# -- Used to check the two separated dataframes
# print(missDF.head(), '\n\n', hitDF.head())

# -- Used to check the combined dataframe
# print(result.shape)

# -- Used to play with matplotlib functionality
# plt.scatter(result['NumBonds'], result['Sequence'])
# plt.show()

result['Label'] = result['Label'].astype(float)
result['Sequence'] = result['Sequence'].astype(float)
result['NumBonds'] = result['NumBonds'].astype(float)
result['Energy'] = result['Energy'].astype(float)

# print(result.dtypes)

from sklearn.model_selection import train_test_split

x = result.drop(['Label'], axis=1)
y = result['Label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
# model.add(Dense(128, activation='relu', input_shape=(None, 3)))
# model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid', input_dim=3))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

hist = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, batch_size=100)

import seaborn as sns

sns.set()

acc = hist.history['accuracy']
val = hist.history['val_accuracy']
epochs = range(1, len(acc) + 1)

# print(len(epochs))
# print(len(acc))

plt.plot(epochs, acc, '-', label='Training Accuracy')
plt.plot(epochs, val, ':', label='Validation Accuracy')
plt.title('Training vs Validation Accuracies')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.plot()
plt.show()

from sklearn.metrics import confusion_matrix

y_predicted = model.predict(x_test) > 0.5
mat = confusion_matrix(y_test, y_predicted)
labels = ['Hit', 'Miss']

sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False, cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.show()
