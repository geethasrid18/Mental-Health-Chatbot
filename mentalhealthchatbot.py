# -*- coding: utf-8 -*-
"""MentalHealthChatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HR1qunoYhOgdGXMpdr7689BPqD_gSL8i
"""



from google.colab import drive
drive.mount('/content/drive')

!pip install nltk tensorflow matplotlib wordcloud

import json
import numpy as np
import random
import nltk
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Load the JSON data from Google Drive
with open('/content/drive/MyDrive/KB.json') as file:
    data = json.load(file)

# Understanding the structure of the dataset
print(json.dumps(data, indent=4))



all_words = ' '.join([w for w in words])

wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# Create training data
training = []
output_empty = [0] * len(classes)

# Create bag of words for each sentence
for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(w.lower()) for w in word_patterns]
    for w in words:
        bag.append(1) if w in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Shuffle the training data
random.shuffle(training)

# Split the training data into features (train_x) and labels (train_y)
train_x = np.array([entry[0] for entry in training])  # Bag of words (features)
train_y = np.array([entry[1] for entry in training])  # One-hot encoded classes (labels)

print("Training data created:")
print(f"Feature set shape: {train_x.shape}")
print(f"Label set shape: {train_y.shape}")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Build the Sequential neural network
model = Sequential()

# Add input layer (with size of bag of words), 128 neurons, and ReLU activation function
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))  # Add dropout to prevent overfitting

# Add hidden layer with 64 neurons
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

# Add output layer with softmax activation for classification into intent categories
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile the model with stochastic gradient descent (SGD) optimizer
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()

# Train the model on the data
hist = model.fit(train_x, train_y, epochs=100, batch_size=5, verbose=1)

# Save the trained model
model.save("/content/drive/MyDrive/chatbot_model.h5")

# Save the model in the recommended Keras format
model.save("/content/drive/MyDrive/chatbot_model.keras")

# Evaluate the model to check accuracy on training data
loss, accuracy = model.evaluate(train_x, train_y)

# Print out the accuracy
print(f"Model Accuracy: {accuracy * 100:.2f}%")

import matplotlib.pyplot as plt

# Plot training accuracy
plt.plot(hist.history['accuracy'])
plt.title('Model Accuracy Over Epochs')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper left')
plt.show()

# Plot training loss
plt.plot(hist.history['loss'])
plt.title('Model Loss Over Epochs')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper left')
plt.show()

# Save the trained model in Keras format
model.save("/content/drive/MyDrive/chatbot_model.keras")