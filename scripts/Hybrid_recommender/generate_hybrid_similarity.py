import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

embeddings = np.load(
    "data/embeddings/hybrid_embeddings.npy"
)

similarity_matrix = cosine_similarity(
    embeddings
)

np.save(
    "data/embeddings/hybrid_similarity.npy",
    similarity_matrix
)

print(
    similarity_matrix.shape
)