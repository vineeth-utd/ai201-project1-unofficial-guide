# The Unofficial Guide — Project 1

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

**Off-Campus Housing Experiences Near Arizona State University (Tempe Campus)**

This project focuses on off-campus housing experiences near Arizona State University's Tempe campus. Students searching for housing often need information about apartment quality, management responsiveness, maintenance issues, safety concerns, noise levels, commute convenience, and overall value for money. While apartment websites primarily advertise amenities and pricing, real resident experiences are scattered across review platforms and online discussions, making it difficult for students to efficiently compare housing options and make informed decisions. This system aims to make those unofficial experiences searchable through a single question-answering interface.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | IMT Desert Palm Village Reviews | ApartmentRatings review page | https://www.apartmentratings.com/az/tempe/imt-desert-palm-village_480968109985281/#ratingsReviews  |
| 2 | Murietta at ASU Reviews | ApartmentRatings review page | https://www.apartmentratings.com/az/tempe/murietta-at-asu_85281/#ratingsReviews |
| 3 | Paseo on University Reviews | ApartmentRatings review page | https://www.apartmentratings.com/az/tempe/paseo-on-university_4809688118852818420/#ratingsReviews |
| 4 | Onnix Reviews | ApartmentRatings review page | https://www.apartmentratings.com/az/tempe/onnix_9199332346275174870/#ratingsReviews |
| 5 | Sentry Tempe Reviews | ApartmentRatings review page | https://www.apartmentratings.com/az/tempe/sentry-tempe_4808942261852824945/ |
| 6 | Apartments to Avoid | Reddit discussion thread (r/ASU) | https://www.reddit.com/r/ASU/comments/13vclht/apartments_to_avoid/ |
| 7 | What Apartments Are Good in Tempe Near ASU? | Reddit discussion thread (r/ASU) | https://www.reddit.com/r/ASU/comments/1np68lm/what_apartments_are_good_in_tempe_near_asu/ |
| 8 | Cheap Apartments Near ASU Tempe Recommendations | Reddit discussion thread (r/ASU) | https://www.reddit.com/r/ASU/comments/1d6osqa/cheap_apartments_near_asu_tempe_recommendations/ |
| 9 | Apartments Near ASU | Reddit discussion thread (r/ASU) | https://www.reddit.com/r/ASU/comments/11efwke/apartments_near_asu/ |
| 10 | Off-Campus Apartments | Reddit discussion thread (r/ASU) | https://www.reddit.com/r/ASU/comments/y6pbzt/offcampus_apartments/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Preprocessing before chunking:**

The raw data collected from Reddit and ApartmentRatings was first stored as JSON files in the `documents/raw` directory. A cleaning pipeline then extracted the actual review and discussion content along with relevant metadata such as apartment name, thread title, author, rating, date, and source URL. The cleaned output was stored as structured text files in the `documents/cleaned` directory, where each review or Reddit comment was represented as a readable review block. The chunking pipeline operates on these cleaned text files rather than the raw JSON data.

The cleaned review blocks were stored together with metadata such as *source platform*, *apartment name* or *discussion title*, *source URL*, *author*, *date*, *rating* (when available), and *chunk position*. This metadata was preserved throughout the pipeline for retrieval and source attribution.

**Chunk configuration:**
- **Chunk size:** 500 characters
- **Overlap:** 100 characters
- **Final chunk count:** 3,213 chunks across all 10 source documents.

**Chunking approach:**

A recursive chunking strategy was used. The splitter first attempts to preserve natural semantic boundaries by splitting at paragraph breaks. If a section is still too large, it falls back to sentence boundaries, and only then uses character-based splitting as a last resort. This approach helps keep complete thoughts, recommendations, and complaints together whenever possible. Short Reddit comments and shorter apartment reviews typically remain intact as a single chunk, while longer reviews are divided only when necessary.

**Why these choices fit your documents:**

The corpus consists primarily of apartment reviews and Reddit discussions. Many Reddit comments are short and self-contained, while ApartmentRatings reviews can span multiple paragraphs and discuss several topics such as maintenance, management, safety, amenities, pricing, and move-in experiences.

A chunk size of 500 characters was chosen because it is usually large enough to preserve a complete recommendation, complaint, or resident experience within a single chunk while still being small enough to support precise retrieval. Larger chunks would risk combining multiple unrelated topics into a single embedding, while smaller chunks could fragment reviews and lose important context.

A 100-character overlap was configured to preserve continuity when longer reviews had to be split. In practice, many Reddit comments and shorter apartment reviews remained as single chunks and therefore did not require overlap. For longer reviews, paragraph-level splits generally did not require overlap because each paragraph often represented a separate observation or topic. When a paragraph was still too large and needed to be split at sentence boundaries, overlap was used to preserve context between adjacent chunks.

Using paragraph-first recursive splitting was particularly important for this dataset because apartment reviews often contain multiple independent observations in separate paragraphs. Preserving those boundaries helps retrieval return focused evidence rather than large mixed-topic chunks.

--- 

## Sample Chunks

The examples below illustrate how the recursive chunking strategy handled reviews and Reddit discussions of different lengths. Short comments often remained as a single chunk, while longer reviews and discussions were split into multiple chunks when necessary.

### Chunk 1 — IMT Desert Palm Village Reviews

**Review split into 2 chunks (showing Chunk 0 of 2)**

> I submitted a work order for my apartment as soon as the office opened in the morning. Adon from Maintenance arrived at my door shortly after. He is always friendly and greets me when I open the door. I explained what I needed, and he understood my requests. He then went to get the necessary parts and returned promptly to complete the work quickly and efficiently. Adon knows his job well and handles work order requests in a timely and effective manner!

**Source:** ApartmentRatings - IMT Desert Palm Village Reviews

---

### Chunk 2 — IMT Desert Palm Village Reviews

**Review split into 3 chunks (showing Chunk 0 of 3)**

> If you're moving from out of state, look no further than Stephanie! She's absolutely amazing at what she does. From our very first conversation, she took the time to thoroughly explain everything about the area, which made me feel so much more comfortable with the move. What I really appreciated was her responsiveness, she was always there to answer my questions and ease my worries. Moving can be super stressful, but Stephanie made the whole process seamless

**Source:** ApartmentRatings - IMT Desert Palm Village Reviews

---

### Chunk 3 — Paseo on University Reviews

**Review split into 4 chunks (showing Chunk 0 of 4)**

> Not great. I have lived here almost 3 years and stuff never gets taken care of. Stove has been broken fir a year, apparently the ability to cook is of no priority. Have had bug issues since we moved in, have had dishwasher replaced 2 times, but my final straw is my ac has been broken for 9 hours now, and IF they have emergency maintenance, there is no way to get ahold of them. No number to call, all you can do is put in a work order online

**Source:** ApartmentRatings - Paseo on University Reviews

---

### Chunk 4 — Reddit: Apartments Near ASU

**Comment split into 3 chunks (showing Chunk 0 of 3)**

> Just don’t go towards Mesa or too far south. A few miles from tempe campus in any direction will be the cheaper but still nice enough options. Head north too far into scottsdale and everything is nice and safe but also one of the most expensive cities to live in the whole US. South scottsdale is okay in price still

**Source:** Reddit — r/ASU - Apartments Near ASU

---

### Chunk 5 — Reddit: Apartments to Avoid

**Single-chunk comment**

> Don't sign with Nexa, scammed us for about $500 at move out and according to more negative reviews citing the same on google and elsewhere, seems this is a common practice for them. Preying mostly on foreign students who when they move out and leave the country cant do anything about it.

**Source:** Reddit — r/ASU - Apartments to Avoid

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

I used **all-MiniLM-L6-v2** from the Sentence Transformers library. This model was chosen because it is free, runs locally, has no API costs or rate limits, and provides good semantic retrieval performance for short to medium-length text. Since the corpus consists primarily of apartment reviews and Reddit discussions written in English, all-MiniLM-L6-v2 provided a good balance between retrieval quality, speed, and simplicity. Its small size also made it practical to embed all 3,213 chunks locally without requiring specialized hardware.

**Production tradeoff reflection:**

For this project, **all-MiniLM-L6-v2** worked well because the corpus is relatively small and all documents are written in English. It provided fast embedding generation and retrieval while running entirely locally. 

If I were deploying the system for real users and cost was not a concern, I would experiment with larger embedding models that may better distinguish between apartment reviews that use very similar language. Many reviews in this dataset discuss common topics such as maintenance, management, safety, and noise, which can make different apartment communities appear semantically similar. A stronger embedding model could potentially improve retrieval precision for those cases. I would also weigh the tradeoff between retrieval quality and latency, since larger models generally require more computation and increase response times. 

Additionally, models with stronger multilingual support would become more valuable if the system expanded beyond English-language reviews, and models that support longer context windows could be useful if future documents contained longer discussions or forum threads.

---

## Retrieval Strategy

The system uses **ChromaDB** as its vector store and **all-MiniLM-L6-v2** embeddings for semantic retrieval. For each query, the system first retrieves the top 10 semantic matches from ChromaDB.

During evaluation, I observed that apartment-specific queries sometimes retrieved reviews from other apartment communities because management and maintenance complaints often use very similar language. To improve retrieval quality, I implemented a property-aware reranking step. When a query explicitly mentions an apartment name, ApartmentRatings chunks associated with that apartment are boosted using metadata, while Reddit chunks are boosted when the apartment name appears in the retrieved text. This helps prioritize apartment-specific evidence while preserving the benefits of semantic retrieval.

The final retrieval stage returns the **top 5** chunks, which are then passed to the generation pipeline.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

Grounding is enforced through a combination of retrieval and a strict system prompt. Before generation, the system retrieves the most relevant chunks from ChromaDB and formats them into a structured context block containing source information and review text. Only this retrieved context is provided to the LLM.

The system prompt explicitly instructs the model to answer only from the retrieved context and avoid using general training knowledge. 

**Key grounding instruction:**

> "Answer ONLY from the retrieved context provided in the user message. Do not use your general training knowledge."

The prompt also instructs the model not to invent apartments, facts, prices, or explanations that are not present in the retrieved context, avoid speculation, and keep responses concise and evidence-based. If the retrieved context does not contain enough information, the model is instructed to respond with: 

> "I don't have enough information on that."

**How source attribution is surfaced in the response:**

Source attribution is handled programmatically rather than relying on the LLM. After retrieval, metadata from the retrieved chunks is used to generate a deduplicated source list that is displayed alongside the answer. The user interface also includes a **Supporting Evidence (Advanced)** section that shows the retrieved chunks and retrieval details for transparency and debugging.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

The table below summarizes the system's responses. Full responses were reviewed during evaluation and are available through the application interface.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What concerns do residents raise about management at Sentry Tempe? | Residents describe poor communication, ignored complaints, slow responses, unresolved maintenance requests, and a lack of urgency in addressing resident concerns. | The system identified complaints about management disregarding resident safety, rude maintenance staff, eviction threats, plumbing issues, and unresolved air conditioning problems. | Partially relevant | Partially accurate |
| 2 | Why do multiple residents recommend avoiding Paseo on University? | Residents mention frequent water shutoffs, roach infestations, maintenance problems, plumbing issues, noisy neighbors, safety concerns, and poor communication from management. | The system highlighted roach infestations, frequent water and plumbing issues, safety concerns, harassment, and lack of security. | Relevant | Partially accurate |
| 3 | What positive experiences do residents mention about IMT Desert Palm Village? | Residents frequently praise the maintenance team for quick responses, helpful leasing staff, smooth move-in experiences, affordability, and friendly customer service. | The system emphasized the property's atmosphere, amenities, responsive staff, helpful leasing office employees, and convenient location. | Relevant | Partially accurate |
| 4 | What complaints are mentioned about Onnix? | Residents report slow maintenance, pest problems, parking issues, water shutoffs, trash problems, high costs, and poor communication from management. | The system identified plumbing problems, laundry room issues, pest infestations, maintenance problems, frequent water shutoffs, and poor management practices. | Relevant | Accurate |
| 5 | What is the average rent for a one-bedroom apartment in downtown Phoenix? | The system should indicate that it does not have enough information because the collected documents focus on apartment reviews and housing experiences near ASU Tempe, not rental market statistics for downtown Phoenix. | The system correctly refused to answer and stated that it did not have enough information. | Off-target | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What concerns do residents raise about management at Sentry Tempe?

**What the system returned:**

The system identified concerns such as rude maintenance staff, unresolved plumbing and air conditioning issues, management disregarding resident safety, and eviction threats. While these concerns were grounded in retrieved reviews, the answer did not fully capture other recurring themes such as poor communication, ignored complaints, slow responses, and lack of urgency from management.

**Root cause (tied to a specific pipeline stage):**

This failure originated in the retrieval stage. The embedding model (all-MiniLM-L6-v2) retrieved reviews from other apartment communities because management and maintenance complaints use very similar language across many apartment complexes. Although property-aware reranking improved retrieval quality, only 2 Sentry Tempe chunks appeared in the top 10 semantic retrieval results. Most of the remaining results came from other apartment communities with similar complaint vocabulary. As a result, the generation step received incomplete Sentry-specific evidence and produced a partially accurate answer that missed some expected management-related concerns such as poor communication, ignored complaints, and slow responses.

**What you would change to fix it:**

I would improve retrieval by combining semantic search with stronger apartment-specific matching. One possible approach would be hybrid retrieval that combines embeddings with keyword or metadata filtering on apartment names. I would also experiment with stronger reranking models that better distinguish complaints belonging to one apartment community from similar complaints discussed in reviews of other communities.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning document served as a useful blueprint throughout development. Defining the document sources, chunking strategy, retrieval approach, evaluation questions, and architecture before writing code made it much easier to build the system incrementally. 

Because each stage of the pipeline was planned in advance, the implementation of one milestone naturally prepared the inputs required for the next milestone. The planning document also provided valuable context when working with AI coding tools, since I could share the relevant sections of the spec and architecture diagram to help the tool understand not only the current task but also how that component fit into the overall system design. This resulted in more accurate code generation and reduced the amount of rework needed later in the project.

**One way your implementation diverged from the spec, and why:**

The original retrieval approach in the spec assumed a straightforward semantic retrieval pipeline that returned the top-k results from ChromaDB. During implementation and evaluation, I observed that apartment-specific queries sometimes retrieved reviews from other apartment communities because management and maintenance complaints use very similar language across properties. 

To improve retrieval quality, I introduced a property-aware reranking step that first retrieves the top 10 semantic matches and then boosts chunks associated with the apartment mentioned in the query before returning the final top 5 results. This change was made based on evaluation results and improved retrieval precision for apartment-specific questions.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* 

  I provided Claude Code with the relevant sections of `planning.md`, including the document sources, chunking strategy, retrieval approach, and architecture diagram. I used Claude in Plan Mode with Thinking enabled and asked it to first generate an implementation plan before making any code changes.

- *What it produced:*

  Claude produced a detailed implementation plan and then generated the core pipeline components, including the ingestion and cleaning pipeline, recursive chunking logic, embedding and ChromaDB storage pipeline, retrieval pipeline, grounded generation pipeline, and Gradio interface. It also generated validation scripts that were used to inspect chunk quality, evaluate retrieval behavior, and test grounded generation.

- *What I changed or overrode:*

  I reviewed the generated plans before allowing implementation and adjusted several design decisions. Rather than generating the entire system at once, I built the project incrementally, validating each pipeline stage before moving to the next. I also reviewed and understood the generated code before running or committing it, rather than accepting it directly. This included inspecting cleaned documents before chunking, reviewing chunk quality before generating embeddings, evaluating retrieval results before implementing generation, and analyzing retrieval failures before introducing property-aware reranking.

  I chose to keep short reviews and Reddit comments as single chunks whenever possible, retained the 500-character chunk size and 100-character overlap after validating chunk quality, and later introduced property-aware reranking when evaluation showed that apartment-specific queries were retrieving reviews from other apartment communities.

**Instance 2**

- *What I gave the AI:*

  I used ChatGPT throughout the project to brainstorm ideas, review implementation decisions, and understand specific concepts and APIs. I discussed topics such as chunking tradeoffs, overlap behavior, retrieval evaluation, ChromaDB APIs, source attribution strategies, and grounded generation techniques.

  For example, I used ChatGPT to better understand how overlap behaved in my recursive chunking implementation, how ChromaDB collections and retrieval APIs worked, and to review retrieval results when evaluating the Sentry Tempe management query.

- *What it produced:*

  ChatGPT provided explanations of technical concepts, feedback on implementation choices, and suggestions for interpreting retrieval and evaluation results. It also helped me reason about why certain retrieval failures were occurring and explained the tradeoffs of different approaches such as changing chunk sizes, metadata filtering, and retrieval reranking.

- *What I changed or overrode:*

  I used the explanations and feedback to validate my own decisions rather than accepting suggestions directly. For example, after reviewing the retrieval results for the Sentry Tempe query, I decided not to change the chunk size or overlap because the issue was caused by semantically similar apartment reviews rather than chunk fragmentation. I also selectively adopted improvements such as property-aware reranking and refined source attribution only after evaluating how they affected the behavior of the system.