import sys
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Make project root importable
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Existing RAG components
# ---------------------------------------------------------

from src.retrieval.hybrid_retriever import (
    HybridRetriever,
)

from src.llm.answer_generator import (
    AnswerGenerator,
)

from src.guardrails import (
    GuardrailPipeline,
)


# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="Hybrid RAG API",
    description="FAISS + Neo4j Hybrid RAG chatbot",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------

class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):

    answer: str

    sources: list[Dict[str, Any]] = []

    graph_entities: list[Dict[str, Any]] = []

    graph_relationships: list[Dict[str, Any]] = []


# ---------------------------------------------------------
# Components
# ---------------------------------------------------------

guardrails = GuardrailPipeline()

hybrid_retriever = None

answer_generator = None


# ---------------------------------------------------------
# Startup
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():

    global hybrid_retriever
    global answer_generator

    print(
        "\n"
        + "=" * 60
    )

    print(
        "STARTING HYBRID RAG API"
    )

    print(
        "=" * 60
    )

    print(
        "\nInitializing Hybrid Retriever..."
    )

    hybrid_retriever = HybridRetriever(
        vector_k=5,
        graph_k=5,
    )

    print(
        "\nInitializing Answer Generator..."
    )

    answer_generator = AnswerGenerator()

    print(
        "\nHybrid RAG API ready."
    )


# ---------------------------------------------------------
# Shutdown
# ---------------------------------------------------------

@app.on_event("shutdown")
def shutdown_event():

    global hybrid_retriever

    if hybrid_retriever:

        hybrid_retriever.close()

    print(
        "\nHybrid RAG API stopped."
    )


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "name": "Hybrid RAG API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "retriever": (
            hybrid_retriever is not None
        ),
        "answer_generator": (
            answer_generator is not None
        ),
    }


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    global hybrid_retriever
    global answer_generator

    # -----------------------------------------------------
    # INPUT GUARDRAIL
    # -----------------------------------------------------

    valid, question = (
        guardrails.validate_input(
            request.question
        )
    )

    if not valid:

        raise HTTPException(
            status_code=400,
            detail=question,
        )

    try:

        # -------------------------------------------------
        # HYBRID RETRIEVAL
        # -------------------------------------------------

        retrieval_result = (
            hybrid_retriever.retrieve(
                question
            )
        )

        # -------------------------------------------------
        # ANSWER GENERATION
        # -------------------------------------------------

        answer = answer_generator.generate(
            question,
            retrieval_result,
        )

        # -------------------------------------------------
        # OUTPUT GUARDRAIL
        # -------------------------------------------------

        valid_output, final_answer = (
            guardrails.validate_output(
                answer
            )
        )

        if not valid_output:

            raise HTTPException(
                status_code=422,
                detail=final_answer,
            )

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = []

        seen = set()

        for chunk in retrieval_result.get(
            "merged_chunks",
            [],
        ):

            chunk_id = chunk.get(
                "chunk_id"
            )

            if not chunk_id:
                continue

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            sources.append(
                {
                    "chunk_id": chunk_id,
                    "source": chunk.get(
                        "source"
                    ),
                    "title": chunk.get(
                        "title"
                    ),
                    "page_start": chunk.get(
                        "page_start"
                    ),
                    "page_end": chunk.get(
                        "page_end"
                    ),
                    "section": chunk.get(
                        "section"
                    ),
                    "retrieval_source": chunk.get(
                        "retrieval_source"
                    ),
                }
            )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return ChatResponse(
            answer=final_answer,
            sources=sources,
            graph_entities=(
                retrieval_result.get(
                    "graph_entities",
                    [],
                )
            ),
            graph_relationships=(
                retrieval_result.get(
                    "graph_relationships",
                    [],
                )
            ),
        )

    except HTTPException:
        raise

    except Exception as e:

        print(
            "\nChat request failed:"
        )

        print(
            type(e).__name__,
            str(e),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The RAG pipeline failed. "
                "Check the backend logs."
            ),
        )