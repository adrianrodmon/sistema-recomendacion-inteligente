import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

visual_embeddings = np.load(
    "data/embeddings/visual_embeddings.npy"
)

text_embeddings = np.load(
    "data/embeddings/text_embeddings.npy"
)

movie_ids_visual = np.load(
    "data/embeddings/movie_ids.npy"
)

text_movie_ids = np.load(
    "data/embeddings/text_movie_ids.npy"
)
#peliculas comunes entre ambos conjuntos de embeddings

common_ids = np.intersect1d(
    movie_ids_visual,
    text_movie_ids
)

print(
    f"Películas comunes: {len(common_ids)}"
)

#Filtrar los embeddings para quedarnos solo con las películas comunes
visual_idx = [
    np.where(
        movie_ids_visual == mid
    )[0][0]
    for mid in common_ids
]

text_idx = [
    np.where(
        text_movie_ids == mid
    )[0][0]
    for mid in common_ids
]

visual_subset = visual_embeddings[
    visual_idx
]

text_subset = text_embeddings[
    text_idx
]

#Normalizar los embeddings
visual_subset = StandardScaler().fit_transform(
    visual_subset
)

text_subset = StandardScaler().fit_transform(
    text_subset
)
#PCA
visual_pca = PCA(
    n_components=128,
    random_state=42
)

text_pca = PCA(
    n_components=128,
    random_state=42
)

visual_reduced = visual_pca.fit_transform(
    visual_subset
)

text_reduced = text_pca.fit_transform(
    text_subset
)

#fusionar los embeddings
hybrid_embeddings = (
    0.5 * visual_reduced
    +
    0.5 * text_reduced
)
#guardar los embeddings híbridos
np.save(
    "data/embeddings/hybrid_embeddings.npy",
    hybrid_embeddings
)

np.save(
    "data/embeddings/hybrid_movie_ids.npy",
    common_ids
)

print(
    hybrid_embeddings.shape
)