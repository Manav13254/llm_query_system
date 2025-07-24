# LLM-Powered Document Ingestion & Query Retrieval System

## Overview

This project offers a production-ready pipeline to ingest complex documents (PDF, DOCX, emails), extract and normalize their text, and enable powerful AI-driven question answering. Built with FastAPI, PostgreSQL, and Pinecone vector search, the system supports real-world enterprise workflows requiring accurate, explainable policy and contract insights.

---

## Features

### Document Ingestion
- Multi-format support: PDF, DOCX, Email (.eml, .msg)
- Robust text extraction using industry-leading Python libraries
- Text cleaning and normalization to improve AI understanding
- Metadata hashing and storage in PostgreSQL for auditability
- REST API endpoints for seamless upload workflows

### Semantic Search & Retrieval
- Intelligent text chunking with overlapping windows to capture context
- Embedding and indexing document fragments for efficient vector search in Pinecone
- Multi-turn, multi-query support with semantic reranking

### AI-powered Answering
- GPT-4 / LLM integration with context-aware prompt engineering
- JSON-function-call enabled structured answers that adhere to domain rules
- Business-logic rule engine implementation for automated eligibility verdicts

### Extensibility and Governance
- Modular architecture for easy addition of new file types and ML models
- Comprehensive audit trail in PostgreSQL with traceable data lineage
- Secure config management using environment variables and `.env` files

---

## Architecture

Your documents pass through these sequential stages:

1. **Upload API**: FastAPI endpoints accept files or URLs.
2. **Extraction**: Parsers cleanly extract raw text from multiple formats.
3. **Normalization & Chunking**: Text is cleaned and split into searchable chunks.
4. **Metadata Recording**: Hashes and metadata logged to PostgreSQL.
5. **Embedding & Vector Storage**: Chunks converted to embeddings and pushed to Pinecone.
6. **Query Pipeline**: User questions are embedded, matched, reranked, then answered.
7. **Response Aggregation**: Structured JSON answers along with trace data returned to the user.

---
