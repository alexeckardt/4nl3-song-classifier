from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class Model:
    def __init__(self):
        # Use TfidfVectorizer for text processing.
        self.vectorizer = TfidfVectorizer()
        # Replace the logistic regression with a Naive Bayes classifier.
        self.model = DecisionTreeClassifier()

    def fit(self, X, y):
        """Train the model.
        
        Args:
            X: Array-like of strings.
            y: Target labels for classes between 1 and 11.
        """
        X = X.ravel()
        y = y.ravel()
        X_transformed = self.vectorizer.fit_transform(X)
        self.model.fit(X_transformed, y)

    def predict(self, X):
        """Predict the labels for the given data.
        
        Args:
            X: List of strings.
            
        Returns:
            Predicted class indices.
        """
        X = X.ravel()
        X_transformed = self.vectorizer.transform(X)
        predicts = self.model.predict(X_transformed)
        print(predicts)
        return predicts
