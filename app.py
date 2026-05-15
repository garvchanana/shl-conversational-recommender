import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.intent_router import classify_intent
from fastapi.responses import JSONResponse

from services.conversation_engine import (
    generate_clarification,
    off_topic_response,
    injection_response,
    build_conversation_context,
    is_refinement_query
)

from services.comparison_engine import (
    compare_assessments
)
from models.schemas import (
    ChatRequest,
    ChatResponse
)

from services.recommendation_engine import (
    generate_recommendations
)


# -----------------------------------
# Initialize FastAPI
# -----------------------------------

app = FastAPI(
    title="SHL Assessment Recommendation API"
)

# -----------------------------------
# Startup Validation
# -----------------------------------

required_files = [
    "embeddings/faiss_index.bin",
    "embeddings/metadata.pkl"
]

for file_path in required_files:

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Missing required file: {file_path}"
        )

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Global Exception Handler
# -----------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    _request,
    _exc
):

    return JSONResponse(
        status_code=500,
        content={
            "reply": "Internal server error.",
            "recommendations": [],
            "end_of_conversation": True
        }
    )

# -----------------------------------
# Health Endpoint
# -----------------------------------

@app.get("/health")
def health():

    return {"status": "ok"}


# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Extract latest user message
    user_messages = [
        msg.content
        for msg in request.messages
        if msg.role == "user"
    ]

    if not user_messages:

        return {
            "reply": "Please provide a hiring requirement.",
            "recommendations": [],
            "end_of_conversation": False
        }

    latest_query = user_messages[-1]

    # Build complete conversational context
    conversation_context = build_conversation_context(
        request.messages
    )

    # -----------------------------------
    # Intent Classification
    # -----------------------------------

    intent = classify_intent(latest_query)

    # -----------------------------------
    # Clarification Flow
    # -----------------------------------

    if intent == "clarification":

        return {
            "reply": generate_clarification(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # Off-topic Refusal
    # -----------------------------------

    if intent == "off_topic":

        return {
            "reply": off_topic_response(),
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------------
    # Prompt Injection Refusal
    # -----------------------------------

    if intent == "prompt_injection":

        return {
            "reply": injection_response(),
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------------
    # Comparison Flow
    # -----------------------------------

    if intent == "comparison":

        comparison = compare_assessments(
            latest_query
        )

        return {
            "reply": comparison,
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # Recommendation Flow
    # -----------------------------------

    # Use full conversation context for refinement handling
    query_for_recommendation = (
        conversation_context
        if is_refinement_query(latest_query)
        else latest_query
    )

    result = generate_recommendations(
        query_for_recommendation
    )
    return result