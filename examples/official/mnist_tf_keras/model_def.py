"""
This example shows how to use Determined to implement an image
classification model for the Fashion-MNIST dataset using tf.keras.

Based on: https://www.tensorflow.org/tutorials/keras/classification
"""
import tensorflow as tf
from tensorflow import keras

from determined.keras import TFKerasTrial, TFKerasTrialContext, adapt_keras_data

import data


class MNISTTrial(TFKerasTrial):
    def __init__(self, context: TFKerasTrialContext) -> None:
        self.context = context

    def build_model(self):
        model = keras.Sequential(
            [
                keras.layers.Flatten(input_shape=(28, 28)),
                keras.layers.Dense(128, activation="relu"),
                keras.layers.Dense(10),
            ]
        )
        model = self.context.wrap_model(model)
        model.compile(
            optimizer="adam",
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=[tf.keras.metrics.SparseCategoricalAccuracy(name="accuracy")],
        )
        return model

    def build_training_data_loader(self):
        train_images, train_labels = data.load_training_data()
        train_images = train_images / 255.0

        batch_size = self.context.get_per_slot_batch_size()
        return adapt_keras_data(x=train_images, y=train_labels, batch_size=batch_size)

    def build_validation_data_loader(self):
        test_images, test_labels = data.load_validation_data()
        test_images = test_images / 255.0

        batch_size = self.context.get_per_slot_batch_size()
        return adapt_keras_data(x=test_images, y=test_labels, batch_size=batch_size)
