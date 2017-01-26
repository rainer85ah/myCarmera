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

from sklearn.metrics import accuracy_score, roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.decomposition.pca import PCA
import numpy as np
import pandas as pd
from ggplot import *


class Net:
    def __init__(self, x_train, x_test):
        self.classifiers = [SVC(),
                            SVC(C=1.0, kernel='linear', degree=2, gamma='auto', coef0=0.015, shrinking=True,
                                probability=False, tol=0.001, cache_size=512, class_weight=None, verbose=False,
                                max_iter=-1, decision_function_shape=None, random_state=None), SVC(gamma=2, C=1),
                            DecisionTreeClassifier(criterion="entropy"),
                            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                            GradientBoostingClassifier(),
                            AdaBoostClassifier(),
                            GaussianNB(),
                            LDA(), QDA(),
                            LogisticRegression(), KNeighborsClassifier(5)
                           ]

        self.X_train = x_train
        self.X_test = x_test
        self.X_train_dense = np.asarray(x_train)
        self.X_test_dense = np.asarray(x_test)
        self.clf_array = []
        self.pred_array = []
        self.prob_array = []
        self.accuracy_array = []

    @staticmethod
    def fit_train_clf_pred_prob(self, y_train, y_test):

        for clf in self.classifiers:
            try:
                print('Clf Fit, Predict and Probability')
                # fit = PCA.fit_transform(self.X_train, Y_train)
                fit = clf.fit(self.X_train, y_train)
                pred = fit.predict(self.X_test)
                prob = fit.predict_proba(self.X_test)[:, 1]
            except Exception:
                # fit = PCA.fit_transform(self.X_train_dense, Y_train)
                fit = clf.fit(self.X_train_dense, y_train)
                pred = fit.predict(self.X_test_dense)
                prob = fit.predict_proba(self.X_test_dense)[:, 1]

            self.clf_array.append(clf)
            self.pred_array.append(pred)
            self.prob_array.append(prob)
            self.accuracy_array.append(accuracy_score(pred, y_test))

        return self

    @staticmethod
    def show_results(self, y_test):
        for i, e in enumerate(self.clf_array):
            print('Predict of ' + e.__class__.__name__ + ' is ' + str(self.pred_array[i]))
            print( 'Probability of ' + e.__class__.__name__ + ' is ' + str(self.prob_array[i]))
            print('Accuracy of ' + e.__class__.__name__ + ' is ' + str(self.accuracy_array[i]))

            fpr, tpr, _ = roc_curve(y_test, self.pred_array[i])
            tmp = pd.DataFrame(dict(fpr=fpr, tpr=tpr))
            g = ggplot(tmp, aes(x='fpr', y='tpr')) + geom_line() + geom_abline(linetype='dashed') + \
                ggtitle('Roc Curve of ' + e.__class__.__name__)
            print(g.__str__())

    @staticmethod
    def best_classifier_value(self):
        p = np.asarray(self.pred_array, dtype='float')
        p_sorted = np.sort(p)
        index = len(p_sorted) - 1
        best_value = self.preds[index]
        return best_value

    @staticmethod
    def best_classifier_name(self, value):
        for i, e in enumerate(self.pred_array):
            if e == value:
                return self.clf_array[i].__class__.__name__


""" ITERATIVE
    # Input and preproccesing data *****
    X_train = trainData
    Y_train = trainLabels
    X_test = testData
    Y_test = testLabels

    # Classifiers Techniques... Implementing for loop... pending..
    c0 = SVC()
    c1 = SVC(kernel='linear', C=0.025)
    c2 = SVC(gamma=2, C=1)

    c3 = DecisionTreeClassifier(criterion="entropy")
    c4 = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)

    c5 = GradientBoostingClassifier()
    c6 = AdaBoostClassifier()

    c7 = LDA()
    c8 = QDA()

    c9 = LogisticRegression()
    c10 = KNeighborsClassifier(5)

    # Training without PCA ..
    c0.fit(X_train,Y_train)
    c1.fit(X_train,Y_train)
    c2.fit(X_train,Y_train)
    c3.fit(X_train,Y_train)
    c4.fit(X_train,Y_train)
    c5.fit(X_train,Y_train)
    c6.fit(X_train,Y_train)
    c7.fit(X_train,Y_train)
    c9.fit(X_train,Y_train)
    c10.fit(X_train,Y_train)

    # Predicting ..
    p0 = c0.predict(X_test)
    p1 = c1.predict(X_test)
    p2 = c2.predict(X_test)
    p3 = c3.predict(X_test)
    p4 = c4.predict(X_test)
    p5 = c5.predict(X_test)
    p6 = c6.predict(X_test)
    p7 = c7.predict(X_test)
    p8 = c8.predict(X_test)
    p9 = c9.predict(X_test)
    p10 = c10.predict(X_test)

    #  Results.. Accuracy
    print "0 - SVC: ", accuracy_score(p0, Y_test)
    print "1 - SVC LINEAR: ", accuracy_score(p1, Y_test)
    print "2 - SVC GANMA 2: ", accuracy_score(p2, Y_test)

    print "3 - Decision Tree: ", accuracy_score(p3, Y_test)
    print "4 - Random Forest: ", accuracy_score(p4, Y_test)

    print "5 - SGD", accuracy_score(p5, Y_test)
    print "6 - ADA BOOST", accuracy_score(p6, Y_test)

    print "7 - LDA: ", accuracy_score(p7, Y_test)
    print "8 - QDA: ", accuracy_score(p8, Y_test)

    print "9 - Logistic Regression: ", accuracy_score(p9, Y_test)
    print "10 - K Neighbors: ", accuracy_score(p10, Y_test)
"""
