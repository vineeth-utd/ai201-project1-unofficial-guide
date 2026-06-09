import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gradio as gr
from src.generation.generator import generate


def ask(question: str):
    if not question.strip():
        return "Please enter a question.", "", ""

    result = generate(question)

    answer = result["answer"]

    sources_md = "\n".join(f"- {s}" for s in result["sources"])

    chunks = result["retrieved_chunks"]
    debug_lines = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        source = meta.get("apartment_name") or meta.get("document_title") or "Unknown"
        platform = meta.get("source_platform", "")
        dist = chunk["distance"]
        boosted = " [BOOSTED]" if chunk.get("boosted") else ""
        debug_lines.append(
            f"**[{i}] {platform} — {source}** | dist={dist:.4f}{boosted}\n\n"
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

    with gr.Accordion("Retrieved Chunks (Debug)", open=False):
        chunks_box = gr.Markdown()

    ask_btn.click(fn=ask, inputs=question_box, outputs=[answer_box, sources_box, chunks_box])
    question_box.submit(fn=ask, inputs=question_box, outputs=[answer_box, sources_box, chunks_box])


if __name__ == "__main__":
    demo.launch()
