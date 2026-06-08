# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
