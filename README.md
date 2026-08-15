# Hybrid RAG Policy Assistant

A hybrid Retrieval-Augmented Generation chatbot using:

- FAISS vector search
- Neo4j knowledge graph
- OpenAI embeddings
- OpenAI LLM
- LangChain
- Input/output guardrails
- Optional NVIDIA NeMo Guardrails
- DeepEval evaluation
- Streamlit UI

---

## Architecture

User
  |
  v
Streamlit
  |
  v
Input Guardrail
  |
  v
Hybrid Retriever
  |
  +---- FAISS
  |
  +---- Neo4j
  |
  v
Merged Context
  |
  v
OpenAI
  |
  v
Output Guardrail
  |
  v
Final Answer