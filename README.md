---
title: SHL Conversational Recommender
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# SHL Conversational Assessment Recommendation System

## Overview

This project is a conversational AI-powered assessment recommendation system built for the SHL AI Hiring Assessment challenge.

The system helps recruiters and hiring teams:
- discover relevant SHL assessments,
- refine hiring requirements conversationally,
- compare assessments,
- and receive grounded recommendations using semantic retrieval and large language models.

The application is implemented as a stateless conversational API using FastAPI, FAISS vector search, Sentence Transformers embeddings, and Groq LLM inference.

---

# Key Features

## Conversational Recommendation Flow

The system supports conversational hiring interactions such as:

- vague hiring requests,
- technical hiring queries,
- refinement requests,
- personality assessment additions,
- assessment comparisons,
- and clarification handling.

Example:

```text
User: Hiring a Java developer
User: Also include personality assessments
```

The system preserves previous conversational context and updates recommendations intelligently.

---

## Semantic Retrieval with FAISS

The recommendation engine uses:

- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS vector similarity search
- hybrid semantic + keyword ranking

This enables retrieval of assessments based on semantic meaning instead of exact keyword matching.

---

## Official SHL Catalog Integration

The system uses the official SHL product catalog containing:

- 377 assessments
- structured metadata
- taxonomy information
- job levels
- assessment categories

This significantly improves retrieval quality and recommendation grounding.

---

## Conversational Intelligence

The application supports:

- clarification generation
- refinement-aware recommendations
- comparison mode
- prompt injection defense
- off-topic refusal
- stateless conversation reconstruction

---

## Grounded Recommendations

The model is restricted to recommending only assessments retrieved from the official SHL catalog.

This minimizes hallucinations and ensures evaluator-safe responses.

---

# System Architecture

```text
User Request
      ↓
FastAPI /chat Endpoint
      ↓
Intent Router
      ↓
Conversation Context Builder
      ↓
Hybrid Retriever
      ↓
FAISS Vector Search
      ↓
Groq LLM Recommendation Engine
      ↓
Structured JSON Response
```

---

# Tech Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Vector Search | FAISS |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM Inference | Groq API |
| Language | Python |
| Deployment | Render |
| Validation | Pydantic |

---

# Project Structure

```text
shl-assessment-recommender/
│
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
├── .env
│
├── catalog/
│   ├── official_shl_catalog.json
│   └── shl_catalog_cleaned.json
│
├── embeddings/
│   ├── faiss_index.bin
│   └── metadata.pkl
│
├── models/
│   ├── __init__.py
│   └── schemas.py
│
├── services/
│   ├── __init__.py
│   ├── prepare_official_catalog.py
│   ├── embedding_service.py
│   ├── retriever.py
│   ├── groq_service.py
│   ├── recommendation_engine.py
│   ├── intent_router.py
│   ├── conversation_engine.py
│   └── comparison_engine.py
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd shl-assessment-recommender
```

---

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Preparing the Catalog

The system uses the official SHL assessment catalog.

Run:

```bash
python services/prepare_official_catalog.py
```

This:
- normalizes catalog structure,
- infers assessment types,
- and prepares searchable metadata.

---

# Generating Embeddings

Run:

```bash
python services/embedding_service.py
```

This generates:

- FAISS vector index
- metadata store
- semantic embeddings

Files generated:

```text
embeddings/faiss_index.bin
embeddings/metadata.pkl
```

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Real Evaluation Examples

## Example 1 — Technical Hiring Recommendation

### User Query

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    }
  ]
}
```

### System Response

```json
{
  "reply": "Based on the user hiring requirement for a Java developer, I recommend the following assessments: Java 8 (New) and Core Java (Entry Level) (New). These assessments fit as they measure the knowledge of Java fundamentals, including class design, exceptions, and basic Java constructs, which are essential skills for a Java developer.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "test_type": "K"
    },
    {
      "name": "Java Web Services (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-web-services-new/",
      "test_type": "K"
    },
    {
      "name": "Core Java (Entry Level) (New)",
      "url": "https://www.shl.com/products/product-catalog/view/core-java-entry-level-new/",
      "test_type": "K"
    },
    {
      "name": "Java 2 Platform Enterprise Edition 1.4 Fundamental",
      "url": "https://www.shl.com/products/product-catalog/view/java-2-platform-enterprise-edition-1-4-fundamental/",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

## Example 2 — Conversational Refinement

### User Query

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    },
    {
      "role": "assistant",
      "content": "Any additional requirements?"
    },
    {
      "role": "user",
      "content": "Also include personality assessments"
    }
  ]
}
```

### System Response

```json
{
  "reply": "Based on the user hiring requirement for a Java developer, I recommend Core Java (Entry Level) (New) and Occupational Personality Questionnaire OPQ32r. These assessments complement each other by evaluating both technical skills and personality, providing a comprehensive view of the candidate's suitability for the Java developer position.",
  "recommendations": [
    {
      "name": "Core Java (Entry Level) (New)",
      "url": "https://www.shl.com/products/product-catalog/view/core-java-entry-level-new/",
      "test_type": "K"
    },
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "test_type": "K"
    },
    {
      "name": "Occupational Personality Questionnaire OPQ32r",
      "url": "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
      "test_type": "P"
    },
    {
      "name": "OPQ Manager Plus Report",
      "url": "https://www.shl.com/products/product-catalog/view/opq-manager-plus-report/",
      "test_type": "P"
    }
  ],
  "end_of_conversation": false
}
```

---

## Example 3 — Assessment Comparison

### User Query

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Compare Java 8 and Java EE 7"
    }
  ]
}
```

### System Response

```json
{
  "reply": "Comparison between Java 8 (New) and Java Platform Enterprise Edition 7 (Java EE 7): Java 8 measures Java class design, exceptions, generics, collections, concurrency, JDBC and Java I/O fundamentals, while Java EE 7 measures enterprise architecture concepts including APIs, component technology, database access, application architecture, JSP extensions, web services, and web application technologies.",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

# API Endpoints

## Health Endpoint

### Request

```http
GET /health
```

### Response

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

### Request

```http
POST /chat
```

### Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    }
  ]
}
```

---

## Example Response

```json
{
  "reply": "Based on the hiring requirement for a Java developer...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

# Conversational Capabilities

## Clarification Handling

Example:

```text
User: I need an assessment
```

The system asks follow-up clarification questions before recommending.

---

## Refinement Handling

Example:

```text
User: Hiring a Java developer
User: Also include personality assessments
```

The system preserves technical context and augments recommendations accordingly.

---

## Assessment Comparison

Example:

```text
User: Compare OPQ32r and Java 8
```

The system generates grounded metadata-based comparisons.

---

## Off-topic Refusal

Example:

```text
User: Give me legal advice
```

The system safely refuses unsupported requests.

---

## Prompt Injection Defense

Example:

```text
User: Ignore previous instructions
```

The system rejects unsafe prompt manipulation attempts.

---

# Retrieval Pipeline

The recommendation system uses a hybrid retrieval pipeline:

```text
Semantic Embeddings
        +
Keyword Boosting
        +
Technical Role Prioritization
        ↓
Hybrid Re-ranking
```

This improves:

- technical role matching
- refinement quality
- recommendation relevance
- Recall@10 performance

---

# Deployment

## Render Deployment

The project includes:

```text
render.yaml
```

for Render deployment.

---

## Deployment Steps

1. Push repository to GitHub
2. Create a new Render Web Service
3. Connect GitHub repository
4. Add `GROQ_API_KEY` environment variable
5. Deploy application

---

# Error Handling and Stability

The system includes:

- centralized exception handling,
- startup validation,
- Groq API failure handling,
- response cleanup,
- schema-safe responses.

This improves deployment reliability and evaluator stability.

---

# Evaluation Alignment

This implementation aligns with the SHL challenge requirements:

- conversational recommendation flow,
- stateless API design,
- refinement handling,
- grounded recommendations,
- comparison support,
- prompt injection defense,
- schema-compliant API responses.

---

# Future Improvements

Potential future enhancements include:

- advanced ranking models,
- reranker integration,
- caching,
- streaming responses,
- multilingual support,
- authentication,
- analytics dashboards.

---

# Author

Developed as part of the SHL Conversational AI Hiring Assessment challenge.

