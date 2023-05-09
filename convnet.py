from numpy import asarray
import os, shutil

imgMiss = Image.open('/Users/shighton/IdeaProjects/rnaML2/src/lib/targetMiss.png')
imgHit = Image.open('/Users/shighton/IdeaProjects/rnaML2/src/lib/targetFind.png')

imgMiss = asarray(imgMiss)
imgHit = asarray(imgHit)

print(imgMiss.shape)
print(imgHit.shape)

tilesMiss = [imgMiss[x:x + 25, y:y + 22] for x in range(0, imgMiss.shape[0], 25) for y in
             range(0, imgMiss.shape[1], 22)]
tilesHit = [imgHit[x:x + 25, y:y + 22] for x in range(0, imgHit.shape[0], 25) for y in range(0, imgHit.shape[1], 22)]

numMiss = 0
numHit = 0

for tile in tilesMiss:
    numMiss += 1
    pilImg = Image.fromarray(tile)
    im1 = pilImg.save("/Users/shighton/PycharmProjects/rnaML3/trainML/targetMiss%s.jpg" % (numMiss))

for tile in tilesHit:
    numHit += 1
    pilImg = Image.fromarray(tile)
    im1 = pilImg.save("/Users/shighton/PycharmProjects/rnaML3/trainML/targetHit%s.jpg" % (numHit))


orig_dir = '/Users/shighton/PycharmProjects/rnaML3/trainML'
base_dir = '/Users/shighton/PycharmProjects/rnaML3/binaryClassRNA'

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')
#os.mkdir(base_dir)
#os.mkdir(train_dir)
#os.mkdir(validation_dir)
#os.mkdir(test_dir)

train_hit_dir = os.path.join(train_dir, 'hit')
train_miss_dir = os.path.join(train_dir, 'miss')
#os.mkdir(train_hit_dir)
#os.mkdir(train_miss_dir)

validation_hit_dir = os.path.join(validation_dir, 'hit')
validation_miss_dir = os.path.join(validation_dir, 'miss')
#os.mkdir(validation_hit_dir)
#os.mkdir(validation_miss_dir)

test_hit_dir = os.path.join(test_dir, 'hit')
test_miss_dir = os.path.join(test_dir, 'miss')
#os.mkdir(test_hit_dir)
#os.mkdir(test_miss_dir)


#fnames = file names
fnames = ['targetHit{}.jpg'.format(i) for i in range(1, 251)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(train_hit_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['targetHit{}.jpg'.format(i) for i in range(251, 376)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(validation_hit_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['targetHit{}.jpg'.format(i) for i in range(376, 501)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(test_hit_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['targetMiss{}.jpg'.format(i) for i in range(1, 251)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(train_miss_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['targetMiss{}.jpg'.format(i) for i in range(251, 376)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(validation_miss_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['targetMiss{}.jpg'.format(i) for i in range(376, 501)]
for fname in fnames:
    src = os.path.join(orig_dir, fname)
    dst = os.path.join(test_miss_dir, fname)
    shutil.copyfile(src, dst)

from keras import layers, models

#simple CNN
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
#model.summary()

from tensorflow import keras
import tensorflow as tf

model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.RMSprop(learning_rate=1e-4), metrics=keras.metrics.Recall())

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    # validation_split=0.2,
    # subset="training",
    # seed=123,
    image_size=(150, 150),
    batch_size=25 #25
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    validation_dir,
    # validation_split=0.2,
    # subset="validation",
    # seed=123,
    image_size=(150, 150),
    batch_size=20 #20
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    # validation_split=0.2,
    # subset="validation",
    # seed=123,
    image_size=(150, 150),
    batch_size=20 #20
)

fitted = model.fit(
    train_ds,
    steps_per_epoch=2, #20,
    epochs=5,
    validation_data=val_ds,
    validation_batch_size=1, #20,
    validation_steps=10
)
model.save('binaryClassRNA.h5')

import matplotlib.pyplot as plt

recall = fitted.history['recall']
vali_recall = fitted.history['val_recall']
loss = fitted.history['loss']
vali_loss = fitted.history['val_loss']
epochs = range(1, len(recall) + 1)

plt.plot(epochs, recall, 'r', label='Training Recall')
plt.plot(epochs, vali_recall, 'b', label='Validation Recall')
plt.title('Training and Validation Recall')
plt.legend()

plt.figure()
plt.plot(epochs, loss, 'r', label='Training Loss')
plt.plot(epochs, vali_loss, 'b', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.show()