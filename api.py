from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import faiss
import pickle

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from rerank import infer_intent, rerank_results

# ===============================
# APP INIT
# ===============================
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Intent-aware assessment recommender using FAISS",
    version="1.0"
)

# Add CORS middleware to allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# LOAD MODEL + DATA
# ===============================
index = faiss.read_index("shl_faiss.index")

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# REQUEST / RESPONSE MODELS
# ===============================
class QueryRequest(BaseModel):
    query: str
    top_k: int = 6

class AssessmentResponse(BaseModel):
    assessment_name: str
    url: str
    test_type: str

# ===============================
# RECOMMEND FUNCTION
# ===============================
def recommend(query: str, top_k: int):
    q_emb = model.encode([query]).astype("float32")

    k = min(10, len(metadata))
    _, I = index.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append({
            "assessment_name": metadata[idx]["assessment_name"],
            "url": metadata[idx]["url"],
            "test_type": metadata[idx]["test_type"]
        })

    intent = infer_intent(query)
    final_results = rerank_results(results, intent, top_k)

    return final_results

# ===============================
# API ENDPOINTS
# ===============================
@app.get("/")
def root():
    return {"message": "SHL Assessment Recommendation API is running"}

@app.get("/health")
def health():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "assessments_loaded": len(metadata)
    }

@app.post("/recommend", response_model=List[AssessmentResponse])
def recommend_assessments(req: QueryRequest):
    return recommend(req.query, req.top_k)
