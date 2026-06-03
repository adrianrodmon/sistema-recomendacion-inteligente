import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import (
    TensorDataset,
    DataLoader
)

X = np.load(
    "data/processed/X_lstm.npy"
)

y = np.load(
    "data/processed/y_lstm.npy"
)

X = torch.LongTensor(X)
y = torch.LongTensor(y)

dataset = TensorDataset(
    X,
    y
)

loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

num_genres = len(
    torch.unique(y)
)

class GenreLSTM(nn.Module):

    def __init__(self):

        super().__init__()

        self.embedding = nn.Embedding(
            num_genres,
            16
        )

        self.lstm = nn.LSTM(
            input_size=16,
            hidden_size=32,
            batch_first=True
        )

        self.fc = nn.Linear(
            32,
            num_genres
        )

    def forward(
        self,
        x
    ):

        x = self.embedding(x)

        output, (
            hidden,
            cell
        ) = self.lstm(x)

        x = self.fc(
            hidden[-1]
        )

        return x


model = GenreLSTM()

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 10

for epoch in range(epochs):

    total_loss = 0

    for batch_X, batch_y in loader:

        optimizer.zero_grad()

        outputs = model(
            batch_X
        )

        loss = criterion(
            outputs,
            batch_y
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch {epoch+1}/{epochs}"
        f" Loss={total_loss:.4f}"
    )

torch.save(
    model.state_dict(),
    "models/genre_lstm.pt"
)

print(
    "\nModelo guardado"
)