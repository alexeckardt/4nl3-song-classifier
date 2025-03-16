import numpy as np
from sklearn.linear_model import LogisticRegression

class Model:
    def __init__(self):
        self.classifier = LogisticRegression()

    def fit(self, X, y):
        """ Train the model.

        Args:
            X: Training data matrix of shape (num-samples, num-features), type np.ndarray.
            y: Training label vector of shape (num-samples), type np.ndarray.
        """
        self.classifier.fit(X, y)

    def predict(self, X):
        """ Predict labels.

        Args:
          X: Data matrix of shape (num-samples, num-features) to pass to the model for inference, type np.ndarray.
        """
        y = self.classifier.predict(X)
        return y
