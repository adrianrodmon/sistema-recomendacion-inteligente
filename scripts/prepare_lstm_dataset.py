import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder

df = pd.read_csv(
    "data/processed/user_genre_sequences.csv"
)

user_sequences = (
    df.groupby("customer_id")["genre"]
      .apply(list)
)

encoder = LabelEncoder()

encoder.fit(df["genre"])

X = []
y = []

window_size = 3

for genres in user_sequences:

    encoded = encoder.transform(genres)

    for i in range(
        len(encoded) - window_size
    ):

        X.append(
            encoded[i:i+window_size]
        )

        y.append(
            encoded[i+window_size]
        )

X = np.array(X)
y = np.array(y)

print("X:", X.shape)
print("y:", y.shape)

np.save(
    "data/processed/X_lstm.npy",
    X
)

np.save(
    "data/processed/y_lstm.npy",
    y
)

with open(
    "data/processed/genre_encoder.pkl",
    "wb"
) as f:
    pickle.dump(
        encoder,
        f
    )