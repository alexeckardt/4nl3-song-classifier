from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class Model:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        # Use multinomial logistic regression with the lbfgs solver.
        self.model = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')

    def fit(self, X, y):
        """Train the model.
        
        Args:
            X: Training data list of strings.
            y: Training label matrix of shape (num_samples, 10), one-hot encoded.
        """
        X = X.to_numpy().ravel()
        X_transformed = self.vectorizer.fit_transform(X)

        # Convert one-hot encoded labels to integer class indices.
        y = y.to_numpy()
        y_labels = np.argmax(y, axis=1)
        
        self.model.fit(X_transformed, y_labels)

    def predict(self, X):
        """Predict the labels for the given data.
        
        Args:
            X: List of strings to predict.
            
        Returns:
            Predicted class indices of shape (num_samples,).
        """
        X = X.to_numpy().ravel()
        predicts = []
        for x in X:
            x_transformed = self.vectorizer.transform([x])
            pred = self.model.predict_proba(x_transformed)
            top_two_indices = np.argsort(pred[0])[-2:][::-1]
            one_hot_pred = [0] * 11
            one_hot_pred[top_two_indices[0]] = 1
            one_hot_pred[top_two_indices[1]] = 1
            predicts.append(one_hot_pred)
        return predicts