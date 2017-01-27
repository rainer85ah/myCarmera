# -*- coding: utf-8 -*-
__author__ = 'Rainer Arencibia'

import os
import cv2
import numpy as np


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


class Proccesing(object):

    def __init__(self):
        pass

    def rotate(self, img, degree):
        """
        Rotate an image by the degree indicated.
        :param img: Numpy Array, Image
        :return: Numpy array, Image, rotated.
        """
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)

        M = cv2.getRotationMatrix2D(center, degree, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        return rotated

    def crop(self, img, x, y, width, height):
        """
        Return the Region of interest.
        :param img: Numpy array
        :return: Numpy array, ROI
        """
        roi = img[y:y+height, x:x+width]
        return roi

    def resize(self, img, width, height):
        """
        Resize with the width and height
        :param img: Numpy array
        :return: Numpy array
        """
        thumbnail = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)  # cv2.INTER_AREA
        return thumbnail

    def resize_width(self, img, width):
        """
        To keep the aspect ratio and the image does not look skewed or distorted.
        We calculate the ratio of the new image.
        :param img: Numpy array
        :param width: Width of the new image.
        :return: Numpy array of resize image.
        """
        r = float(width) / img.shape[1]
        dim = (width, int(img.shape[0] * r))
        thumbnail = cv2.resize(img, dsize=dim, interpolation=cv2.INTER_AREA)  # cv2.INTER_AREA
        return thumbnail

    def variance_of_laplacian(self, img):
        """
        Compute the Laplacian of the image and then return the focus,
        measure, which is simply the variance of the Laplacian.
        :return: variance of the Laplacian
        """
        if len(img.shape) == 3:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(img, cv2.CV_64F).var()

    def detection(self, img, detector):
        """
        Detect and Count how many faces are in the image
        :param image: Numpy array
        :return: Integer
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detections = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in detections:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return len(detections), img

    def hist_curve(self, img, gray_color=False):
        bins = np.arange(256).reshape(256, 1)
        h = np.zeros((300, 256, 3))
        color = None

        if gray_color is True:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if len(img.shape) == 2:
            color = [(255, 255, 255)]
        elif img.shape[2] == 3:
            color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([img], [ch], None, [256], [0, 256])
            cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
            hist = np.int32(np.around(hist_item))
            pts = np.int32(np.column_stack((bins, hist)))
            cv2.polylines(h, [pts], False, col)

        y = np.flipud(h)
        return y, img

    def hist_lines(self, img, normalize=False, equalize=False):
        """
        hist_lines applicable only for gray-scale images.
        :param img: Numpy array
        :return: Two Numpy Arrays: Lines Hist and the gray scale of the image.
        First, Gray, 2 Normalize and 3-Equalize
        """
        h = np.zeros((300, 256, 3))
        if len(img.shape) != 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if normalize is True:
            img = cv2.normalize(img, dst=img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        if equalize is True:
            img = cv2.equalizeHist(img)

        hist_item = cv2.calcHist([img], [0], None, [256], [0, 256])
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))

        for x, y in enumerate(hist):
            cv2.line(h, (x, 0), (x, y), (255, 255, 255))
        y = np.flipud(h)
        return y, img

if __name__ == '__main__':

    os.chdir('/home/rainer85ah/Desktop/source/data/')
    thumbnail_url = '/home/rainer85ah/Desktop/source/thumbnail/'
    processing = Proccesing()
    # ext = [".jpg", ".png"]
    # images_list = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(ext)]
    """
    for i, img in enumerate(os.listdir(os.getcwd())):
        name = img.title()
        img = cv2.imread(img)
        img = processing.resize_width(img, 640)
        cv2.imwrite(thumbnail_url+name, img)
    """
    os.chdir(thumbnail_url)
    # This value is high with the intention of not allow images with a bad quality. "Blur, Dark, etc."
    threshold = 600.0
    url = '/home/rainer85ah/Software/opencv-3.1.0/data/haarcascades/haarcascade_eye.xml'
    for i, img in enumerate(os.listdir(os.getcwd())):
        image = cv2.imread(img)
        variance = processing.variance_of_laplacian(image)
        text = 'Not Blurry: '
        if variance < threshold:
            text = 'Blurry: '

        cv2.putText(image, "{} {:.2f}".format(text, variance), (10, 30), cv2.QT_FONT_NORMAL, 0.8, (0, 255, 0), 1)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)

        """
        We are going to code inside the for loop to filter and only apply the classification to good quality images.
        Eye detector.. It's a general classifier for eyes from OpenCV.
        We can create a new detector with much more accuracy for faces, cars, tags, street signals, etc..
        """
        if variance > threshold:
            detector = cv2.CascadeClassifier(url)
            number, img = processing.detection(image, detector)
            cv2.putText(img, "{} {:}".format('Detections: ', number), (10, 60), cv2.QT_FONT_NORMAL, 0.8, (0, 255, 0), 1)
            cv2.imshow("Image", img)
            key = cv2.waitKey(0)

        """
        Some basic images operations. Rotate, Crop and Resize with width and height.
        """
        """
        image = processing.rotate(image, 90)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)

        center_y = image.shape[0]/2
        center_x = image.shape[1] / 2
        image = processing.crop(image, center_y, center_x, center_y+50, center_x+50)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)

        image = processing.resize(image, 128, 128)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)
        """
        """
        More basic images operations to get Information from the images.
        Histogram of color and gray-scale images.
        """
        """
        curve_hist, _ = processing.hist_curve(image, gray_color=False)
        cv2.imshow('Curve Histogram - Color Image', curve_hist)
        cv2.waitKey(0)

        curve_hist, gray = processing.hist_curve(image, gray_color=True)
        cv2.imshow('Curve Histogram - Gray Image', curve_hist)
        cv2.imshow('GrayScale Image', gray)
        cv2.waitKey(0)

        lines_hist, gray = processing.hist_lines(image, normalize=False, equalize=False)
        cv2.imshow('Lines Histogram - Gray Image', lines_hist)
        cv2.imshow('GrayScale Image', gray)
        cv2.waitKey(0)

        lines_hist, norm = processing.hist_lines(image, normalize=True, equalize=False)
        cv2.imshow('Lines Histogram Normalize', lines_hist)
        cv2.imshow('Image Normalized', norm)
        cv2.waitKey(0)

        lines_hist, equalized = processing.hist_lines(image, normalize=False, equalize=True)
        cv2.imshow('Lines Histogram Equalize', lines_hist)
        cv2.imshow('Image Equalize', equalized)
        cv2.waitKey(0)

        lines_hist, norm_equa = processing.hist_lines(image, normalize=True, equalize=True)
        cv2.imshow('Lines Histogram Normalized Image', lines_hist)
        cv2.imshow('Normalized + Equalized Image', norm_equa)
        cv2.waitKey(0)
        """
