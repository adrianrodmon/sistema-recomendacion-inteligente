import pandas as pd

df = pd.read_csv(
    "data/processed/movies_clean.csv"
)

sample_df = df.sample(
    1000,
    random_state=42
)

sample_df.to_csv(
    "data/processed/movies_sample_1000.csv",
    index=False
)
print(sample_df.shape)