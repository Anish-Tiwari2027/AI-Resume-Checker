from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_similarity(resume_text, jd_text):
    """
    Computes cosine similarity between resume and job description
    using TF-IDF vectors.
    """
    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)
