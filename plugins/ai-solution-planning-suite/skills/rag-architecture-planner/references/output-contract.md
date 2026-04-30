# RAG Architecture Planner Output Contract

```yaml
rag_architecture:
  rag_id: ""
  knowledge_sources:
    - source: ""
      owner: user|project|organization|external
      sensitivity: low|medium|high
      retention: ""
  ingestion_pipeline:
    chunking: ""
    metadata:
      - ""
    indexing: ""
  retrieval_strategy:
    query_rewrite: ""
    retrieval: ""
    reranking: ""
    citation: ""
  permission_rules:
    - ""
  fallback_rules:
    - ""
  rag_eval:
    - case: ""
      expected_behavior: ""
```
