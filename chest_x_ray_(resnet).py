# -*- coding: utf-8 -*-
"""Chest_X_Ray_(ResNET).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oLRZNftZUY0K1y7OPBX9-71m2N6tkhNK
"""

!pip install kaggle
from google.colab import files

# Upload kaggle.json for Kaggle authentication
files.upload()  # Upload kaggle.json

# Setup Kaggle API credentials
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Download the dataset from Kaggle
!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

# Unzip the dataset to the correct directory
!unzip chest-xray-pneumonia.zip -d /content



import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import numpy as np # Providing mathmatical funcitons
import os # Directing file directories
import matplotlib.pyplot as plt # For visualizaitons

from keras import Sequential # Stacking layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator # Giving batches of images
from tensorflow.keras.applications import MobileNet # Pre-trained model for image classification
from tensorflow.keras.layers import Dense, Dropout # Neural network layer drop out layers randomly to be avoid overfitting
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adamax # During training optimize the model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint # Automatic stop to prevent overfitting
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc # Computing ROC curve and providing confusion matrix and other metrics

base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model to prevent training on pre-trained weights
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.5),  # Dropout for regularization
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),  # Another Dropout layer
    layers.Dense(1, activation='sigmoid')  # Binary classification (pneumonia or not)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

IMG_HEIGHT , IMG_WIDTH = 224, 224
# Creating an Imagedatagenerator to set up parameters as well as divided the dataset like test-train-validaiton

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.25,
    height_shift_range=0.25,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest',
    validation_split = 0.2 # Using 20 percetnage of the training data for validation part.
) # rescale,rotation range and other parameters which can make more robust the dataset against to various conditions.

val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
     '/content/chest_xray/chest_xray/train',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=32,
    class_mode='binary',  #'categorical' option can be used when there are more than two classes
    subset = 'training'
)

val_generator = train_datagen.flow_from_directory(
     '/content/chest_xray/chest_xray/val',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=32,
    class_mode='binary',
    subset = 'validation',
    shuffle = True # help better generalizaiton as well as minimize overfitting
)

test_generator = test_datagen.flow_from_directory(
     '/content/chest_xray/chest_xray/test',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=32,
    class_mode='binary',
     shuffle=False
)

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
lr_reduction = ReduceLROnPlateau(monitor='val_loss', patience=3, factor=0.2, min_lr=1e-6)

history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=20,
    validation_data=val_generator,
    validation_steps=len(val_generator),
    callbacks=[early_stopping, lr_reduction]
)

test_loss, test_acc = model.evaluate(test_generator, steps=len(test_generator))
print(f"Test Accuracy: {test_acc}")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# True labels from the test set
true_labels = test_generator.classes

# Receiving predicted probabilities from the model
predictions = model.predict(test_generator)

# Convert predicted probabilities to binary class labels (0 or 1)
predicted_labels = np.round(predictions).astype(int).reshape(-1)

# Compute confusion matrix
cm = confusion_matrix(true_labels, predicted_labels)

# Plot the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=test_generator.class_indices.keys())

# Display the matrix
disp.plot(cmap=plt.cm.Blues)
plt.show()

# Plot training and validation accuracy as graphically
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training and validation loss values as graphically
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.show()

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
os.listdir('/content/chest_xray/chest_xray/train')
predictions = model.predict(test_generator)
predictions = np.round(predictions).astype(int)

# Compherensive benchmark score of the training step
print(classification_report(test_generator.classes, predictions))
print(confusion_matrix(test_generator.classes, predictions))
fpr, tpr, thresholds = roc_curve(test_generator.classes, predictions)
roc_auc = auc(fpr, tpr)