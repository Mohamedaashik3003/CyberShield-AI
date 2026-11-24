
import joblib
import pandas as pd
import faiss
from pathlib import Path
from transformers import pipeline
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "models"

best_model = joblib.load(MODEL_DIR / "cybershield_model.pkl")
encoder = joblib.load(MODEL_DIR / "protocol_encoder.pkl")

feature_columns = [
    "duration", "protocol", "src_bytes",
    "dst_bytes", "failed_logins", "connection_count"
]

security_classifier = pipeline(
    "zero-shot-classification",
    model="valhalla/distilbart-mnli-12-1",
    device=-1
)

threat_labels = [
    "a brute-force attack using repeated failed login attempts to guess passwords",
    "network port scanning to discover open ports on a server",
    "a denial-of-service attack overwhelming a server with excessive requests",
    "normal network activity with legitimate user login behavior"
]

security_docs = [
    "Brute-force attacks involve repeated login attempts to guess a user's password. Multiple failed logins from one IP address may indicate this activity.",
    "Port scanning identifies open ports and services on a network. Unusual connection attempts across many ports may indicate reconnaissance.",
    "Denial-of-service attacks overwhelm a server with excessive requests, making services unavailable to legitimate users.",
    "Normal network activity includes legitimate user logins and expected data transfers.",
    "Repeated authentication failures should be investigated using timestamps, source IP addresses, account activity, and authentication logs.",
    "Network monitoring can identify unusual connection counts and unexpected traffic patterns.",
    "Security alerts are indicators for investigation, not proof of malicious activity."
]

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

document_embeddings = embedding_model.encode(
    security_docs,
    convert_to_numpy=True
)

vector_db = faiss.IndexFlatL2(document_embeddings.shape[1])
vector_db.add(document_embeddings.astype("float32"))


def analyze_security_event(event, features):

    features["protocol"] = encoder.transform(
        [features["protocol"]]
    )[0]

    input_data = pd.DataFrame(
        [features],
        columns=feature_columns
    )

    ml_prediction = best_model.predict(input_data)[0]

    nlp_result = security_classifier(
        event,
        candidate_labels=threat_labels,
        hypothesis_template="This cybersecurity event is an example of {}."
    )

    query_embedding = embedding_model.encode(
        [event],
        convert_to_numpy=True
    )

    distances, indices = vector_db.search(
        query_embedding.astype("float32"), 3
    )

    intelligence = [
        security_docs[i] for i in indices[0] if i != -1
    ]

    return {
        "ml_detection": "Suspicious" if ml_prediction == 1 else "Normal",
        "nlp_classification": nlp_result["labels"][0],
        "nlp_score": round(float(nlp_result["scores"][0]) * 100, 2),
        "security_intelligence": intelligence
    }
