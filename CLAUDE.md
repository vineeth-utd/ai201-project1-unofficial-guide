# The Unofficial Guide

Read planning.md first. It is the source of truth for the project design.

## Repo Structure

### Project Files

- app.py -> Gradio user interface and application entry point
- planning.md -> project specification and implementation plan
- README.md -> project documentation, evaluation results, and reflections

### Data and Storage

- assets/ -> architecture diagram

- documents/raw/reddit/ -> raw Reddit JSON
- documents/raw/apartmentratings/ -> raw ApartmentRatings JSON

- documents/cleaned/reddit/ -> cleaned Reddit text files
- documents/cleaned/apartmentratings/ -> cleaned ApartmentRatings text files

- documents/chunks.json -> chunked corpus with metadata

- documents/chroma_db/ -> persistent ChromaDB vector store

### Source Code

- src/ingestion/ -> ingestion, normalization, and chunking code
  - reddit_extractor.py -> Reddit-specific extraction and normalization
  - apartmentratings_extractor.py -> ApartmentRatings extraction and normalization
  - pipeline.py -> ingestion and cleaning pipeline
  - chunker.py -> recursive chunking pipeline

- src/embedding/ -> embedding and vector store code
  - vectorstore.py -> embedding generation and ChromaDB storage
  - retriever.py -> semantic retrieval and property-aware reranking

- src/generation/ -> grounded answer generation
  - generator.py -> retrieval-to-LLM generation pipeline

## Source Rules

- Reddit and ApartmentRatings have different JSON structures.
- Do not assume the same keys exist in both.
- One raw source document should become one cleaned text file.

## Cleaning Format

- Keep metadata with each comment/review block.
- Preserve source URL, title/property name, author, date, rating if available, and management response if available.

## Chunking

Implemented and validated.

- Recursive chunking
- Chunk size: 500 characters
- Overlap: 100 characters
- Paragraph → sentence → character fallback
- Keep short reviews/comments intact whenever possible
- Split long reviews at natural boundaries before character splitting

Chunk output:
- documents/chunks.json

## Chunk Metadata

Each chunk preserves metadata for retrieval, filtering, debugging, and source attribution.

**Metadata fields:**

- source_platform
- source_url
- author
- record_type
- document_title
- apartment_name
- thread_title
- rating
- review_title
- date
- chunk_index

Chunk text is stored separately in the `text` field.

**Notes:**

- ApartmentRatings chunks populate:
  - apartment_name
  - rating
  - review_title

- Reddit chunks populate:
  - thread_title

- Fields that do not apply to a source may be null.

## Embeddings

Implemented and validated.

- Embedding model: all-MiniLM-L6-v2
- Chunk source: documents/chunks.json
- Vector store: ChromaDB
- Persistent storage: documents/chroma_db/

Only the chunk text field is embedded.

Chunk metadata is stored separately in ChromaDB for retrieval and source attribution.

## ChromaDB Management

**Default behavior:**

```bash
python3 src/embedding/vectorstore.py
```

- Reuses the existing ChromaDB collection if it already exists.

**Rebuild behavior:**

```bash
python3 src/embedding/vectorstore.py --rebuild
```

- Deletes the existing collection.
- Regenerates embeddings from documents/chunks.json.
- Recreates the ChromaDB collection from scratch.

## Retrieval

Implemented and validated.

- Embedding model: all-MiniLM-L6-v2
- Vector store: ChromaDB
- Final top-k: 5

Retrieval process:

1. Retrieve the top 10 semantic matches from ChromaDB.
2. Detect whether the query explicitly mentions an apartment property.
3. Apply property-aware reranking:
   - ApartmentRatings chunks are boosted when apartment_name matches.
   - Reddit chunks are boosted when the apartment name appears in the chunk text.
4. Return the final top 5 results.
5. Retrieved chunks are passed to the generation pipeline.
6. Source attribution is generated programmatically from chunk metadata.
7. Duplicate sources are consolidated into a single citation entry before display.

Property-aware reranking is only applied when the query explicitly mentions an apartment property. Otherwise, retrieval uses pure semantic search.

## Generation

Implemented and validated.

- LLM: Groq llama-3.3-70b-versatile
- Answers must be grounded only in retrieved context.
- Do not use external knowledge when retrieved context is insufficient.
- If retrieved context does not contain enough information, respond:
  "I don't have enough information on that."

Source attribution is handled programmatically rather than relying on the LLM.

Generation output includes:
- Deduplicated source attribution.
- Citation remapping when multiple retrieved chunks originate from the same source.
- A refusal response when retrieved context is insufficient.
- A Supporting Evidence section exposing retrieved chunks and retrieval details for debugging and transparency.

## User Interface

Implemented and validated.

Input:
- Housing-related question entered through a Gradio textbox.

Outputs:
- Answer
- Sources Used
- Supporting Evidence (Advanced)

Supporting Evidence displays:
- Retrieved chunks
- Retrieval distance scores
- Property-aware reranking indicators
- Chunk-to-source mappings

The interface is intended to provide both a simple user-facing experience and transparency into the retrieval process.

## Evaluation

Implemented and documented in README.

Evaluation consists of:
- Five predefined test questions from planning.md
- Retrieval quality assessment
- Response accuracy assessment
- Failure case analysis

Known failure case:
- Apartment-specific management queries may retrieve reviews from other apartment communities when semantically similar management complaints dominate retrieval results.

## Development Notes

- Prefer simple, readable code.
- Evaluate retrieval quality before modifying generation behavior.
- Prefer fixing retrieval issues at the retrieval layer rather than compensating in prompts.
- Update planning.md only if the actual implementation changes.