import tensorflow as tf
from tensorflow import keras

# fashion_mnist = keras.datasets.fashion_mnist
# (train_images, train_lables),(test_images,test_lables) = fashion_mnist.load_data()

model = keras.Sequential([
    keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(28,28,1))
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Conv2D(64, (3,3), activation='relu')
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax'),
])

# model.compile(
#     optimizer=tf.train.AdamOptimizer(),
#     loss='sparse_categorical_crossentropy'
# )

# model.fit(train_images, train_lables, epochs=5)

# test_loss,test_acc = model.evaluate(test_images, test_lables)

# predications = model.predict(my_images)


