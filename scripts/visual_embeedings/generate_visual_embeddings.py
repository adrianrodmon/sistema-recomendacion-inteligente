import os
import numpy as np
import pandas as pd

from PIL import Image

import torch
import torchvision.transforms as transforms

from torchvision.models import (
    resnet50,
    ResNet50_Weights
)

POSTERS_DIR = "data/posters"

OUTPUT_DIR = "data/embeddings"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

df = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

weights = ResNet50_Weights.DEFAULT

model = resnet50(
    weights=weights
)

model.fc = torch.nn.Identity()

model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

embeddings = []
movie_ids = []

with torch.no_grad():

    for _, row in df.iterrows():

        movie_id = row["id"]

        image_path = os.path.join(
            POSTERS_DIR,
            f"{movie_id}.jpg"
        )

        if not os.path.exists(
            image_path
        ):
            continue

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            tensor = transform(
                image
            ).unsqueeze(0)

            embedding = model(
                tensor
            )

            embeddings.append(
                embedding.squeeze().numpy()
            )

            movie_ids.append(
                movie_id
            )

        except Exception:
            continue

embeddings = np.array(
    embeddings
)

movie_ids = np.array(
    movie_ids
)

np.save(
    "data/embeddings/visual_embeddings.npy",
    embeddings
)

np.save(
    "data/embeddings/movie_ids.npy",
    movie_ids
)

print(
    f"Embeddings generados: {len(embeddings)}"
)

print(
    f"Dimension: {embeddings.shape}"
)