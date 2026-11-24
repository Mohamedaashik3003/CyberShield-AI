
# CyberShield AI

AI-powered cybersecurity threat detection and security intelligence platform.

## Features
- Machine Learning-based suspicious event detection.
- Hugging Face zero-shot threat classification.
- FAISS-based security knowledge retrieval.
- Retrieval-Augmented Generation (RAG).
- FastAPI backend.
- Streamlit interactive dashboard.
- Simulated cybersecurity event analysis.

## Technology Stack
Python, Pandas, NumPy, Scikit-learn, PyTorch,
Hugging Face Transformers, Sentence Transformers,
FAISS, FastAPI, Streamlit.

## Project Structure
- data/: Dataset storage
- models/: Trained ML models
- notebooks/: Development notebooks
- src/: Detection and intelligence modules
- app/api/: FastAPI backend
- app/dashboard/: Streamlit dashboard
- tests/: Testing
- docs/: Documentation

## Run Locally

Activate the environment:

    conda activate cybershield

Start the API from the project root:

    uvicorn app.api.main:app --reload

Start the dashboard in a second terminal:

    streamlit run app/dashboard/dashboard.py

API documentation:
http://127.0.0.1:8000/docs

Dashboard:
http://localhost:8501

## Important Limitations
This academic project currently uses simulated security events.
Its model scores are not calibrated probabilities.
Predictions are indicators for investigation, not proof of an attack.
Security intelligence should be verified by a human analyst.

## Project Status
Core ML, NLP, RAG, API and dashboard integration completed.
