import os
import re

from dotenv import load_dotenv
from google import genai


load_dotenv()


def read_tasks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def ensure_three_sentences(text):
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if len(sentences) >= 3:
        return " ".join(sentences[:3])

    return text.strip()


def generate_ai_standup(done_tasks, in_progress_tasks):
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY")
    except (FileNotFoundError, KeyError):
        pass

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from .env"
        )

    client = genai.Client(
        api_key=api_key
    )

    done_text = "\n".join(
        f"- {task}"
        for task in done_tasks
    )

    progress_text = "\n".join(
        f"- {task}"
        for task in in_progress_tasks
    )

    prompt = f"""
You are a Daily Stand-up Reporter.

Create exactly 3 professional sentences.

Sentence 1:
Summarize the completed tasks.

Sentence 2:
Summarize the in-progress tasks.

Sentence 3:
Summarize the developer's current focus.

Rules:
- Return exactly 3 sentences.
- Do not use bullet points.
- Do not use headings.
- Do not invent tasks.
- Do not invent blockers.
- Do not invent deadlines.
- Keep the wording concise and professional.

DONE TASKS:
{done_text}

IN PROGRESS TASKS:
{progress_text}
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )

    if not interaction.output_text:
        raise ValueError(
            "Gemini returned no text."
        )

    result = interaction.output_text.strip()

    return ensure_three_sentences(result)