# Required Libraries
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.datasets import mnist
from keras.layers import Dense, Flatten, Reshape, LeakyReLU
from keras.models import Sequential
from keras.optimizers import Adam

# Function to build the generator model
def build_generator(img_shape, zdim):
    model = Sequential()
    model.add(Dense(128, input_dim=zdim))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dense(28*28*1, activation='tanh'))
    model.add(Reshape(img_shape))
    return model

# Function to build the discriminator model
def build_discriminator(img_shape):
    model = Sequential()
    model.add(Flatten(input_shape=img_shape))
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Function to build the GAN model
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# Function to train the GAN model
def train_gan(generator, discriminator, gan, iterations, batch_size, interval):
    # Load the dataset
    (X_train, _), (_, _) = mnist.load_data()
    # Rescale the images to the range [-1, 1]
    X_train = X_train / 127.5 - 1.0
    X_train = np.expand_dims(X_train, axis=3)
    # Define the labels for real and fake images
    real_labels = np.ones((batch_size, 1))
    fake_labels = np.zeros((batch_size, 1))
    # Lists to store losses and accuracies for plotting
    d_losses, g_losses, accuracies, iteration_checks = [], [], [], []
    # Train the model for the given number of iterations
    for iteration in range(iterations):
        # Select a random batch of real images from the dataset
        ids = np.random.randint(0, X_train.shape[0], batch_size)
        real_images = X_train[ids]
        # Generate a batch of fake images from the generator
        noise = np.random.normal(0, 1, (batch_size, 100))
        fake_images = generator.predict(noise)
        # Train the discriminator on the real and fake images
        d_loss_real = discriminator.train_on_batch(real_images, real_labels)
        d_loss_fake = discriminator.train_on_batch(fake_images, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        accuracy = 100 * np.mean(discriminator.predict(real_images) >= 0.5)
        # Train the generator by fooling the discriminator
        noise = np.random.normal(0, 1, (batch_size, 100))
        g_loss = gan.train_on_batch(noise, real_labels)
        # Append the losses and accuracies for plotting
        if (iteration + 1) % interval == 0:
           
