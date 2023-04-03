# Import required libraries
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.datasets import mnist
from keras.layers import Dense, Flatten, Reshape
from keras.layers.activation import LeakyReLU
from keras.models import Sequential
from keras.optimizers import Adam
import streamlit as st

# Define image dimensions
img_rows = 28     
img_cols = 28
channels = 1
img_shape = (img_rows, img_cols, channels)

# Define latent space dimension
zdim = 100

# Define generator model
def build_gen(img_shape, zdim):
    model = Sequential()
    model.add(Dense(128, input_dim=zdim))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dense(28*28*1, activation='tanh'))
    model.add(Reshape(img_shape))
    return model

# Define discriminator model
def build_dis(img_shape):
    model = Sequential()
    model.add(Flatten(input_shape=img_shape))
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Define GAN model
def build_gan(gen, dis):
    model = Sequential()
    model.add(gen) 
    model.add(dis)
    return model

# Compile discriminator model
dis_v = build_dis(img_shape)
dis_v.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Compile generator model
gen_v = build_gen(img_shape, zdim)
dis_v.trainable = False

# Compile GAN model
gan_v = build_gan(gen_v, dis_v)
gan_v.compile(loss='binary_crossentropy', optimizer=Adam())

# Initialize empty lists for losses, accuracies, and iteration checkpoints
losses = []
accuracies = []
iteration_checks = []

# Define training function
def train(iterations, batch_size, interval):
    # Load MNIST dataset
    (Xtrain , _ ), (_,_) = mnist.load_data()
    Xtrain = Xtrain / 127.5 - 1.0
    Xtrain = np.expand_dims(Xtrain, axis=3)

    # Define real and fake labels
    real = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    for iteration in range(iterations):
        # Select a random batch of images
        ids = np.random.randint(0, Xtrain.shape[0], batch_size)
        imgs = Xtrain[ids]

        # Generate a batch of fake images
        z = np.random.normal(0, 1, (batch_size, 100))
        gen_imgs = gen_v.predict(z)

        # Train the discriminator on real and fake images
        dloss_real = dis_v.train_on_batch(imgs, real)
        dloss_fake = dis_v.train_on_batch(gen_imgs, fake)
        dloss, accuracy = 0.5 * np.add(dloss_real, dloss_fake)

        # Train the generator by fooling the discriminator
        z = np.random.normal(0, 1, (batch_size, 100))
        gloss = gan_v.train_on_batch(z, real)

        # Save loss, accuracy, and iteration checkpoint
        if (iteration + 1) % interval == 0:
            losses.append((dloss, gloss))
            accuracies.append(100.0 * accuracy)
            iteration_checks.append(iteration + 1)

            # Display generated images
            show_images
