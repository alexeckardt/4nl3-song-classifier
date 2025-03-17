import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

class Model:
    def __init__(self):
        self.num_words = 10000
        self.max_len = 100
        self.embedding_dim = 128
        self.lstm_units = 64
        self.num_topics = 11
        self.tokenizer = keras.preprocessing.text.Tokenizer(num_words=self.num_words)
        self._build_model()

    def _build_model(self):
        self.model = keras.Sequential([
            layers.Embedding(input_dim=self.num_words, output_dim=self.embedding_dim, input_length=self.max_len),
            layers.LSTM(self.lstm_units),
            layers.Dense(self.num_topics, activation='sigmoid')
        ])
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def fit(self, X, y, epochs=5, batch_size=32):
        X = X.to_numpy().ravel()
        self.tokenizer.fit_on_texts(X)
        sequences = self.tokenizer.texts_to_sequences(X)
        padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=self.max_len)
        padded_sequences = padded_sequences.astype('int32')
        y = np.array(y, dtype='float32')
        self.model.fit(padded_sequences, y, epochs=epochs, batch_size=batch_size)

    def predict(self, X):
        X = X.to_numpy().ravel()
        sequences = self.tokenizer.texts_to_sequences(X)
        padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=self.max_len)
        probs = self.model.predict(padded_sequences)
        preds = []
        for p in probs:
            top2_idx = p.argsort()[-2:]
            pred_vector = [0] * self.num_topics
            for i in top2_idx:
                pred_vector[i] = 1
            preds.append(pred_vector)
        return preds
