## 1
# Import tensorflow packages
import tensorflow as tf
import numpy as np

# MNIST data loading and preprocessing
mnist = tf.keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print("train_images = ", train_images)
print("length =", len(train_images))
print("type(train_images) = ", type(train_images))

print('Before reshaping....')
print(np.shape(train_images)) # (60000, 28, 28)

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

print('After reshaping....')
print(np.shape(train_images)) # (60000, 28, 28, 1)

## 2
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model.summary()

## 3
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)

## 4
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
