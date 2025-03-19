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
        pass

    def fit(self, X, y):
        """ Train the model.

        Args:
            X: Training data matrix of shape (num-samples), type np.ndarray.
            y: Training label vector of shape (num-samples), type np.ndarray.
        """
        
        self.vocab = build_vocab_from_iterator(map(self.tokenize, X), specials=["<PAD>", "<UNK>"])
        self.vocab.set_default_index(self.vocab['<UNK>'])
        sequences = [torch.tensor([self.vocab[token] for token in self.tokenize(text)]) for text in X]
        padded_sequences = pad_sequence(sequences, batch_first=True, padding_value=self.vocab["<PAD>"])
        dataset = TensorDataset(padded_sequences, y)
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

        self.classifier = LSTM(len(self.vocab))
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.classifier.parameter(), lr=0.01)

        num_epochs = 10
        for epoch in range(num_epochs):
            for batch_texts, batch_labels in dataloader:
                optimizer.zero_grad()
                outputs = self.classifier(batch_texts)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()

    def predict(self, X):
        """ Predict labels.

        Args:
          X: Data matrix of shape (num-samples, num-features) to pass to the model for inference, type np.ndarray.
        """
        self.classifier.eval()
        with torch.no_grad():
            seq = torch.tensor([self.vocab[token] for token in self.tokenize(X)]).unsqueeze(0)
            padded_seq = pad_sequence([seq], batch_first=True, padding_value=self.vocab["<PAD>"])
            output = self.classifier(padded_seq)
            predicted_class = torch.argmax(output, dim=1).item()
        return predicted_class
    
    def tokenize(text):
        return text.lower().split()

class LSTM(nn.Module):
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