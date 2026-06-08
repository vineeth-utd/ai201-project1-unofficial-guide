# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
**Off-Campus Housing Experiences Near Arizona State University (Tempe Campus)**

This project focuses on off-campus housing experiences near Arizona State University's Tempe campus. Students searching for housing often need information about apartment quality, management responsiveness, maintenance issues, safety concerns, noise levels, commute convenience, and overall value for money. While apartment websites primarily advertise amenities and pricing, real resident experiences are scattered across review platforms and online discussions, making it difficult for students to efficiently compare housing options and make informed decisions. This system aims to make those unofficial experiences searchable through a single question-answering interface.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | IMT Desert Palm Village Reviews | ApartmentRatings reviews discussing resident experiences, management quality, maintenance, safety, and amenities. | https://www.apartmentratings.com/az/tempe/imt-desert-palm-village_480968109985281/#ratingsReviews  |
| 2 | Murietta at ASU Reviews | ApartmentRatings reviews covering maintenance issues, safety concerns, management interactions, and overall resident satisfaction. | https://www.apartmentratings.com/az/tempe/murietta-at-asu_85281/#ratingsReviews |
| 3 | Paseo on University Reviews | ApartmentRatings reviews describing apartment conditions, noise levels, management responsiveness, and resident experiences. | https://www.apartmentratings.com/az/tempe/paseo-on-university_4809688118852818420/#ratingsReviews |
| 4 | Onnix Reviews | ApartmentRatings reviews discussing amenities, maintenance quality, leasing experiences, and resident feedback. | https://www.apartmentratings.com/az/tempe/onnix_9199332346275174870/#ratingsReviews |
| 5 | Sentry Tempe Reviews | ApartmentRatings reviews highlighting safety, maintenance, management, pricing, and overall housing experiences. | https://www.apartmentratings.com/az/tempe/sentry-tempe_4808942261852824945/ |
| 6 | Apartments to Avoid | Reddit discussion where ASU students share apartments they recommend avoiding and explain common issues. | https://www.reddit.com/r/ASU/comments/13vclht/apartments_to_avoid/ |
| 7 | What Apartments Are Good in Tempe Near ASU? | Reddit discussion containing apartment recommendations and comparisons from current and former students. | https://www.reddit.com/r/ASU/comments/1np68lm/what_apartments_are_good_in_tempe_near_asu/ |
| 8 | Cheap Apartments Near ASU Tempe Recommendations | Reddit discussion focused on affordable housing options, pricing, and value for money near campus. | https://www.reddit.com/r/ASU/comments/1d6osqa/cheap_apartments_near_asu_tempe_recommendations/ |
| 9 | Apartments Near ASU | Reddit discussion covering general housing recommendations, apartment experiences, and location considerations. | https://www.reddit.com/r/ASU/comments/11efwke/apartments_near_asu/ |
| 10 | Off-Campus Apartments | Reddit discussion about off-campus housing options, apartment comparisons, and student experiences living near ASU. | https://www.reddit.com/r/ASU/comments/y6pbzt/offcampus_apartments/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:**
My documents contain a mix of ApartmentRatings reviews and Reddit discussions. Some reviews are only one or two sentences long, while others are several paragraphs and cover multiple topics such as safety, maintenance, management, and pricing.

I plan to use a recursive chunking strategy so that shorter reviews and comments stay intact whenever possible. For longer reviews, the text will be split at natural boundaries such as paragraphs or sentences before falling back to character-based splitting. I chose a chunk size of 500 characters because it is usually large enough to keep a complete recommendation or complaint together, while still being small enough for accurate retrieval. I will use an overlap of 100 characters so that important details are less likely to be lost when a long review is split across multiple chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 (sentence-transformers)

**Top-k:** 5

**Production tradeoff reflection:**
For this project, I will use all-MiniLM-L6-v2 because it is free, runs locally, and is fast enough for a small RAG system. I chose a top-k value of 5 because it should provide enough context from multiple reviews and discussions without introducing too much unrelated information. If I were deploying this system for real users and cost was not a constraint, I would consider larger embedding models that may provide better retrieval accuracy, especially for longer reviews and more complex housing-related queries. I would also consider latency, since larger models are often slower, and multilingual support if the system needed to handle reviews written in languages other than English. Since all of my current documents are in English, multilingual support is not a requirement for this project.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which apartment communities are most commonly recommended near ASU, and why? | IMT Desert Palm Village is frequently recommended because of responsive maintenance staff, helpful leasing staff, affordability, and positive resident experiences. Other recommendations include Park Place, Union, Oliv, Redpoint, The Regency, and Southbank Apartments for reasons such as location, amenities, management quality, or affordability. |
| 2 | Why do multiple residents recommend avoiding Paseo on University? | Residents mention frequent water shutoffs, roach infestations, maintenance problems, plumbing issues, noisy neighbors, safety concerns, and poor communication from management. |
| 3 | What positive experiences do residents mention about IMT Desert Palm Village? | Residents frequently praise the maintenance team for quick responses, helpful leasing staff, smooth move-in experiences, affordability, and friendly customer service. |
| 4 | What complaints are mentioned about Onnix? | Residents report slow maintenance, pest problems, parking issues, water shutoffs, trash problems, high costs, and poor communication from management. |
| 5 | What is the average rent for a one-bedroom apartment in downtown Phoenix? | The system should indicate that it does not have enough information because this topic is outside the scope of the collected documents. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Challenge 1: Conflicting Opinions** - Apartment reviews and Reddit discussions are highly subjective. One resident may describe an apartment as quiet and safe, while another may describe the same apartment as noisy and unsafe. This could make it difficult for the system to provide a clear answer when the retrieved chunks contain conflicting experiences from different residents.


2. **Challenge 2: Long Reviews Cover Multiple Topics** - Many ApartmentRatings reviews discuss several topics in a single review, such as maintenance, safety, management, pricing, and amenities. If a long review is split into multiple chunks, important context could be separated across chunk boundaries, causing retrieval to return only part of a resident's experience and leading to incomplete answers.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I plan to use Claude Code to help build the cleaning and chunking scripts. I will give it my Documents section, Chunking Strategy section, and the pipeline diagram so it knows what file types I have and how I want the text to be processed. I expect it to produce scripts that load the raw JSON/text files, clean the content, and split it into chunks using my chosen chunk size and overlap. I will verify the output by printing cleaned documents and a few sample chunks to make sure the text still reads naturally and that reviews/comments are not getting broken in awkward places.

**Milestone 4 — Embedding and retrieval:**

I plan to use Claude Code to implement the embedding and retrieval part of the pipeline. I will give it my Retrieval Approach section, Chunking Strategy section, and Architecture diagram so it can connect the cleaned chunks to the vector store correctly. I expect it to produce code that embeds the chunks with all-MiniLM-L6-v2, stores them in ChromaDB with source metadata, and returns the top-k most relevant chunks for a query. I will verify this by testing a few evaluation questions and checking whether the retrieved chunks are actually relevant and come from the right sources.

**Milestone 5 — Generation and interface:**

I plan to use Claude Code to wire retrieval into the LLM and build the query interface. I will give it my Retrieval Approach section, Anticipated Challenges, and Architecture diagram, along with my grounding requirement that answers must come only from retrieved context. I expect it to produce a working end-to-end query flow that retrieves chunks, sends them to the model, and returns an answer with source attribution. I will verify the output by asking questions that are clearly covered by the documents, checking that the response cites the correct sources, and also asking at least one out-of-scope question to make sure the system refuses instead of guessing.
