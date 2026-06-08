# The Unofficial Guide

Read planning.md first. It is the source of truth for the project design.

## Repo structure

- assets/ -> architecture diagram
- documents/raw/reddit/ -> raw Reddit JSON
- documents/raw/apartmentratings/ -> raw ApartmentRatings JSON
- documents/cleaned/reddit/ -> cleaned Reddit text files
- documents/cleaned/apartmentratings/ -> cleaned ApartmentRatings text files
- src/ingestion/ -> ingestion and normalization code

## Source rules

- Reddit and ApartmentRatings have different JSON structures.
- Do not assume the same keys exist in both.
- One raw source document should become one cleaned text file.

## Cleaning format

- Keep metadata with each comment/review block.
- Preserve source URL, title/property name, author, date, rating if available, and management response if available.

## Chunking

- Recursive chunking
- Chunk size: 500 characters
- Overlap: 100 characters
- Keep short reviews/comments intact whenever possible

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