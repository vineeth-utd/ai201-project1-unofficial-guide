import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gradio as gr
from src.generation.generator import generate


REFUSAL = "I don't have enough information on that."


def ask(question: str):
    if not question.strip():
        return "Please enter a question.", "", ""

    try:
        result = generate(question)
    except Exception as e:
        return f"An unexpected error occurred: {e}", "", ""

    # Normalize LLM citation style: "(Source: [N])" → "[N]"
    answer = re.sub(r'\(Source:\s*\[(\d+)\]\)', r'[\1]', result["answer"])

    chunks = result["retrieved_chunks"]

    # Build deduplication maps in a single pass over chunks.
    # label_to_num:  source label → deduplicated citation number (1-based)
    # chunk_to_num:  chunk position (1-based) → deduplicated citation number
    # dedup_sources: deduplicated citation number → (label, url)
    label_to_num = {}
    chunk_to_num = {}
    dedup_sources = {}

    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        name = meta.get("apartment_name") or meta.get("document_title") or "Unknown"
        platform = meta.get("source_platform", "")
        url = meta.get("source_url", "")
        label = f"{platform} — {name}"

        if label not in label_to_num:
            num = len(label_to_num) + 1
            label_to_num[label] = num
            dedup_sources[num] = (label, url)

        chunk_to_num[i] = label_to_num[label]

    # Remap [N] citations in the answer to deduplicated numbers.
    def remap(m):
        orig = int(m.group(1))
        return f"[{chunk_to_num.get(orig, orig)}]"

    answer = re.sub(r'\[(\d+)\]', remap, answer)

    # User-facing source list: deduplicated, with clickable links, no chunk indices.
    is_refusal = answer.strip() == REFUSAL
    heading = "**Retrieved Context (Insufficient to Answer)**" if is_refusal else "**Sources Used**"
    source_lines = []
    for num in sorted(dedup_sources):
        label, url = dedup_sources[num]
        source_lines.append(f"[{num}] [{label}]({url})" if url else f"[{num}] {label}")
    sources_md = heading + "\n\n" + "\n\n".join(source_lines)

    # Debug section: per-chunk details preserved in full.
    debug_lines = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        name = meta.get("apartment_name") or meta.get("document_title") or "Unknown"
        platform = meta.get("source_platform", "")
        label = f"{platform} — {name}"
        dist = chunk["distance"]
        boosted = " [BOOSTED]" if chunk.get("boosted") else ""
        chunk_idx = meta.get("chunk_index", "?")
        debug_lines.append(
            f"**[chunk {i} → source {chunk_to_num[i]}] {label}** | dist={dist:.4f}{boosted} | chunk_idx={chunk_idx}\n\n"
            f"{chunk['text']}"
        )
    chunks_md = "\n\n---\n\n".join(debug_lines)

    return answer, sources_md, chunks_md


with gr.Blocks(title="The Unofficial Guide — ASU Off-Campus Housing") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk questions about off-campus apartments near ASU Tempe.")

    with gr.Row():
        question_box = gr.Textbox(
            label="Your Question",
            placeholder="e.g. What do residents say about management at Sentry Tempe?",
            lines=2,
            scale=4,
        )
        ask_btn = gr.Button("Ask", variant="primary", scale=1)

    answer_box = gr.Textbox(label="Answer", lines=6, interactive=False)
    sources_box = gr.Markdown(label="Sources")

    with gr.Accordion("Supporting Evidence (Advanced)", open=False):
        chunks_box = gr.Markdown()

    ask_btn.click(fn=ask, inputs=question_box, outputs=[answer_box, sources_box, chunks_box])
    question_box.submit(fn=ask, inputs=question_box, outputs=[answer_box, sources_box, chunks_box])


if __name__ == "__main__":
    demo.launch()
