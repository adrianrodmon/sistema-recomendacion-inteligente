import pickle
import torch
import torch.nn as nn
import numpy as np

with open(
    "data/processed/genre_encoder.pkl",
    "rb"
) as f:
    encoder = pickle.load(f)

num_genres = len(
    encoder.classes_
)

class GenreLSTM(nn.Module):

    def __init__(self):

        super().__init__()

        self.embedding = nn.Embedding(
            num_genres,
            16
        )

        self.lstm = nn.LSTM(
            16,
            32,
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

        _, (
            hidden,
            _
        ) = self.lstm(x)

        return self.fc(
            hidden[-1]
        )

model = GenreLSTM()

model.load_state_dict(
    torch.load(
        "models/genre_lstm.pt"
    )
)

model.eval()

sequence = [
    "Action",
    "Comedy",
    "Drama"
]

encoded = encoder.transform(
    sequence
)

x = torch.LongTensor(
    [encoded]
)

with torch.no_grad():

    prediction = model(
        x
    )

predicted_class = prediction.argmax(
    dim=1
).item()

genre = encoder.inverse_transform(
    [predicted_class]
)[0]

print(
    f"Siguiente género: {genre}"
)