import fitz
import json
from prompts import resume_embedding, jd_embedding
from llm import llm


def extract_text(file_path):
    doc = fitz.open(file_path)
    pages = []

    for page in doc:
        pages.append(page.get_text())

    return "\n".join(pages)


def clean_json(text):
    text = text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


def formatted_resume(state):
    raw_resume = state["raw_resume"]

    prompt = resume_embedding(raw_resume)

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    output = response.choices[0].message.content
    output = clean_json(output)

    parsed_resume = json.loads(output)

    return {
        "parsed_resume": parsed_resume
    }


def formatted_jds(state):
    raw_jds = state["raw_jds"]

    all_jds = "\n\n---JD---\n\n".join(raw_jds)

    prompt = jd_embedding(all_jds)

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    output = response.choices[0].message.content
    output = clean_json(output)

    parsed_jds = json.loads(output)

    return {
        "parsed_jds": parsed_jds
    }
