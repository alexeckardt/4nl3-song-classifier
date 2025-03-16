# model

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchtext.vocab import build_vocab_from_iterator
from torch.nn.utils.rnn import pad_sequence

class Model:
    def __init__(self):
        """ <ADD DOCUMENTATION HERE>
        """
        self.classifier = LTSM()

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

class LTSM(nn.Module):
    # code from tutorial:
    def __init__(self, vocab_size, embed_dim=16, hidden_dim=32, num_tags=11, pad_idx=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx)
        self.lstm = nn.LSTM(input_size=embed_dim, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_tags)

    def forward(self, x):
        embeds = self.embedding(x)       # => (batch_size, seq_len, embed_dim)
        lstm_out, _ = self.lstm(embeds)  # => (batch_size, seq_len, hidden_dim)
        logits = self.fc(lstm_out)       # => (batch_size, seq_len, num_tags)
        return logits