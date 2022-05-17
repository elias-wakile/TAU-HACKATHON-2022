from __future__ import annotations
from typing import NoReturn
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, precision_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.cluster import KMeans
import tensorflow

class MondayMLModel:
    """
    An estimator for solving the Difficulty and Time Challenge
    """

    def __init__(self):
        """
        Instantiate an estimator for solving the Difficulty and Time Challenge challenge
        Parameters
        ----------
        Attributes
        ----------
        """
        self._models = [
                        SVC(kernel='rbf'),
                        Ridge(),
                        RandomForestClassifier(n_estimators=300,
                                               max_depth=1,
                                               min_samples_split=0.03,
                                               min_weight_fraction_leaf=0.06,
                                               min_samples_leaf=9, bootstrap=True
                                               ), #
                        KNeighborsClassifier(n_neighbors=300, algorithm='ball_tree', leaf_size=200)
        ]

    def fit(self, X: np.ndarray, y: np.ndarray) -> NoReturn:
        """
        Fit an estimator for given samples
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data to fit an estimator for
        y : ndarray of shape (n_samples, )
            Responses of input data to fit to
        Notes
        -----
        """
        for model in self._models:
            model.fit(X, y)


    def predict(self, X: np.ndarray, time=None) -> np.ndarray:
        """
        Predict responses for given samples using fitted estimator
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data to predict responses for
        Returns
        -------
        responses : ndarray of shape (n_samples, )
            Predicted responses of given samples
        """
        predicts = np.zeros((np.shape(X)[0], np.shape(self._models)[0]))
        for index, model in enumerate(self._models):
            predicts[:, index] = model.predict(X)
        predicts = np.mean(predicts, axis=1)
        if time:
            predicts /= 60
        predicts = np.round(predicts)
        return predicts

    def accuracy(self, y_pred: np.ndarray, y_true: np.ndarray):
        """
            Evaluate performance under loss function
            Parameters
            ----------
            y_pred : ndarray of shape (n_samples, )
                Predicted labels of test samples
            y_true : ndarray of shape (n_samples, )
                True labels of test samples
            Returns
            -------
            accuracu : float
                accuracy
        """
        return np.count_nonzero(np.abs(y_pred - np.round(y_true)) <= 1) / y_pred.shape[0]


