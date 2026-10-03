from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compare_contracts(text1, text2):

    if not text1.strip() or not text2.strip():
        return {
            "score": 0,
            "percentage": 0,
            "message": "Both contracts are required."
        }

    documents = [
        text1.strip(),
        text2.strip()
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    percentage = round(
        similarity * 100,
        2
    )

    if percentage >= 80:
        message = "The contracts have a very high textual similarity."

    elif percentage >= 60:
        message = "The contracts have a high textual similarity."

    elif percentage >= 40:
        message = "The contracts have a moderate textual similarity."

    elif percentage >= 20:
        message = "The contracts have a low textual similarity."

    else:
        message = "The contracts have very little textual similarity."

    return {
        "score": round(similarity, 4),
        "percentage": percentage,
        "message": message
    }