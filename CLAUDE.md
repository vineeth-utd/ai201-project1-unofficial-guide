# The Unofficial Guide

Read planning.md first. It is the source of truth for the project design.

## Repo structure

- assets/ -> architecture diagram

- documents/raw/reddit/ -> raw Reddit JSON
- documents/raw/apartmentratings/ -> raw ApartmentRatings JSON

- documents/cleaned/reddit/ -> cleaned Reddit text files
- documents/cleaned/apartmentratings/ -> cleaned ApartmentRatings text files

- documents/chunks.json -> chunked corpus with metadata

- documents/chroma_db/ -> persistent ChromaDB vector store

- src/ingestion/ -> ingestion, normalization, and chunking code
  - reddit_extractor.py -> Reddit-specific extraction and normalization
  - apartmentratings_extractor.py -> ApartmentRatings extraction and normalization
  - pipeline.py -> ingestion and cleaning pipeline
  - chunker.py -> recursive chunking pipeline

- src/embedding/ -> embedding and vector store code
  - vectorstore.py -> embedding generation and ChromaDB storage

## Source rules

- Reddit and ApartmentRatings have different JSON structures.
- Do not assume the same keys exist in both.
- One raw source document should become one cleaned text file.

## Cleaning format

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

- Embedding model: all-MiniLM-L6-v2
- Vector store: ChromaDB
- top-k: 5

## Generation

- Use Groq llama-3.3-70b-versatile
- Answer only from retrieved context
- Include source attribution
- Refuse out-of-scope questions

## Development notes

- Prefer simple, readable code.
- Validate outputs before moving to the next stage.
- Update planning.md only if the actual implementation changes.