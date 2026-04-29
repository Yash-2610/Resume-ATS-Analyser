import json
import re
from llm import llm
from prompts import smart_gap_analysis_prompt


def extract_json(text):

    text = str(text).strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return "{}"


def to_clean_string(value):

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip().lower()

    if isinstance(value, dict):

        # common keys
        for key in ["skill", "name", "value", "title"]:
            if key in value:
                return str(value[key]).strip().lower()

        return str(value).strip().lower()

    if isinstance(value, list):

        if len(value) == 0:
            return ""

        return str(value[0]).strip().lower()

    return str(value).strip().lower()


def clean_skill_list(items):

    final = []

    if not isinstance(items, list):
        return final

    for item in items:

        val = to_clean_string(item)

        if val:
            final.append(val)

    # remove duplicates
    return list(dict.fromkeys(final))


def clean_weight_dict(weights):

    final = {}

    if not isinstance(weights, dict):
        return final

    for k, v in weights.items():

        key = to_clean_string(k)

        try:
            val = int(v)
        except:
            val = 1

        if key:
            final[key] = val

    return final


def smart_gap_analysis(state):

    parsed_resume = state["parsed_resume"]
    selected_jd = state["selected_jd"]

    resume_skills = parsed_resume["skills"]
    projects = parsed_resume["projects"]

    prompt = smart_gap_analysis_prompt(
        resume_skills,
        projects,
        selected_jd
    )

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content

    json_text = extract_json(raw_output)

    try:
        result = json.loads(json_text)
    except:
        result = {}


    matched_skills = clean_skill_list(
        result.get("matched_skills", [])
    )

    missing_skills = clean_skill_list(
        result.get("missing_skills", [])
    )

    related_skills = clean_skill_list(
        result.get("related_skills", [])
    )

    skill_weights = clean_weight_dict(
        result.get("skill_weights", {})
    )

    total_weight = sum(skill_weights.values())

    matched_weight = 0

    for skill in matched_skills:
        if skill in skill_weights:
            matched_weight += skill_weights[skill]

    if total_weight == 0:
        score = 0
    else:
        score = round((matched_weight / total_weight) * 100, 2)


    score = min(score + min(len(related_skills) * 3, 10), 100)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "related_skills": related_skills,
        "skill_weights": skill_weights,
        "match_score": score
    }