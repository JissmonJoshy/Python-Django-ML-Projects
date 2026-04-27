from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Products

# Load pretrained deep learning NLP model
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_product_search(query, top_n=10):
    """
    ML-based semantic product search
    """

    # Fetch products
    products = Products.objects.all()

    if not products.exists():
        return Products.objects.none()

    product_texts = []
    product_ids = []

    for p in products:
        text = f"{p.name} {p.type} {p.desc}"
        product_texts.append(text)
        product_ids.append(p.id)

    # Convert products to embeddings (ML)
    product_embeddings = model.encode(product_texts)

    # Convert search query to embedding
    query_embedding = model.encode([query])

    # Compute similarity
    similarity_scores = cosine_similarity(query_embedding, product_embeddings)[0]

    # Get top matching products
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]
    matched_ids = [product_ids[i] for i in top_indices]

    return Products.objects.filter(id__in=matched_ids)