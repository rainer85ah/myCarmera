# -*- coding: utf-8 -*-
__author__ = 'Rainer Arencibia'
"""
MIT License

Copyright (c) 2016 Rainer Arencibia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from IPython.display import SVG
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Activation, Flatten, Dense, Dropout
from keras.models import Sequential
from keras.utils.visualize_util import model_to_dot
from keras.utils.visualize_util import plot
from keras.optimizers import SGD, Adagrad, Adadelta, Adam

class NN:
    def __init__(self):
        pass

    @staticmethod
    def build(width, height, depth, classes, weights_path=None):
        """
        :param width: the width of the input images
        :param height: the height of the input images
        :param depth:  the depth of the input images
        :param classes: the numbers of labels
        :param weights_path: URL of an already trained model.
        :return: a train model.
        """
        # initialize the model..
        model = Sequential()

        # first set of CONV => RELU => POOL
        model.add(Convolution2D(32, 5, 5, border_mode="same", bias=True, input_shape=(depth, height, width)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # second set of CONV => RELU => POOL => Dropout
        model.add(Convolution2D(64, 5, 5, border_mode="same", bias=True))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Dropout(0.25))

        # set of FC => RELU layers
        model.add(Flatten())  # convert convolutional filters to flatt so they can be feed to fully connected layers

        # first fully connected layer
        model.add(Dense(400, init='lecun_uniform', bias=True))  # init='glorot_uniform'
        model.add(Activation("relu"))
        model.add(Dropout(0.25))

        # second fully connected layer.. softmax classifier
        model.add(Dense(classes, init='lecun_uniform', bias=True))
        model.add(Activation("softmax"))

        # if a weights path is supplied (indicating that the model was pre-trained), then load the weights.
        if weights_path is not None:
            model.load_weights(weights_path)

        SVG(model_to_dot(model).create(prog='dot', format='svg'))
        plot(model, to_file='/home/rainer85ah/Desktop/Carmera/model.jpg', show_shapes=False, show_layer_names=True)
        print("Check.. '/home/rainer85ah/Desktop/Carmera/model.jpg' file.")

        """
        In my own experience, Adagrad / Adadelta are "safer" because they don't depend so strongly on setting of
        learning rates(with Adadelta being slightly better), but well - tuned SGD + Momentum almost always
        converges faster and at better final values.

        Adadelta is a gradient descent based learning algorithm that adapts the learning rate per parameter over time.
        Adadelta It is similar to rmsprop and can be used instead of vanilla SGD.
        opt = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08)
        """
        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        return model
