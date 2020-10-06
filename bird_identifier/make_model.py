import pandas as pd
import os

from sklearn.utils import class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout, Activation
from tensorflow.keras.layers import BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten, Dropout, Activation, LSTM, SimpleRNN, Conv1D, Input, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

infile = 'samples_df.csv'
samples_df = pd.read_csv(infile)

#print(samples_df.bird.unique())
#import sys
#sys.exit(0)

training_percentage = 0.9
training_item_count = int(len(samples_df)*training_percentage)
validation_item_count = len(samples_df)-int(len(samples_df)*training_percentage)
training_df = samples_df[:training_item_count]
validation_df = samples_df[training_item_count:]

classes_to_predict = sorted(samples_df.bird.unique())
input_shape = (216,216, 3)
effnet_layers = EfficientNetB0(weights=None, include_top=False, input_shape=input_shape)

for layer in effnet_layers.layers:
    layer.trainable = True

dropout_dense_layer = 0.3

model = Sequential()
model.add(effnet_layers)

model.add(GlobalAveragePooling2D())
model.add(Dense(256, use_bias=False))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(dropout_dense_layer))

model.add(Dense(len(classes_to_predict), activation="softmax"))

print(model.summary())


callbacks = [ReduceLROnPlateau(monitor='val_loss', patience=2, verbose=1, factor=0.7),
             EarlyStopping(monitor='val_loss', patience=5),
             ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)]
model.compile(loss="categorical_crossentropy", optimizer='adam')

class_weights = class_weight.compute_class_weight("balanced", classes_to_predict, samples_df.bird.values)
class_weights_dict = {i : class_weights[i] for i,label in enumerate(classes_to_predict)}

training_batch_size = 32
validation_batch_size = 32
target_size = (216,216)

train_datagen = ImageDataGenerator(
    rescale=1. / 255
)

train_generator = train_datagen.flow_from_dataframe(
    dataframe = training_df,
    x_col='song_sample',
    y_col='bird',
    directory='.',
    target_size=target_size,
    batch_size=training_batch_size,
    shuffle=True,
    class_mode='categorical')

validation_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = validation_datagen.flow_from_dataframe(
    dataframe = validation_df,
    x_col='song_sample',
    y_col='bird',
    directory='.',
    target_size=target_size,
    shuffle=False,
    batch_size=validation_batch_size,
    class_mode='categorical')


history = model.fit(train_generator,
          epochs = 20,
          validation_data=validation_generator,
#           class_weight=class_weights_dict,
          callbacks=callbacks)


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss over epochs')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='best')
plt.show()
plt.savefig('keras_train_validation_error.png')


preds = model.predict_generator(validation_generator)
validation_df = pd.DataFrame(columns=["prediction", "groundtruth", "correct_prediction"])

for pred, groundtruth in zip(preds[:16], validation_generator.__getitem__(0)[1]):
    validation_df = validation_df.append({"prediction":classes_to_predict[np.argmax(pred)],
                                       "groundtruth":classes_to_predict[np.argmax(groundtruth)],
                                       "correct_prediction":np.argmax(pred)==np.argmax(groundtruth)}, ignore_index=True)
validation_df.to_csv('keras_validation_df.csv')

