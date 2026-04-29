import json
from llm import llm
from prompts import resume_selection_prompt


def resume_suggestions(state):

    selected_jd = state["selected_jd"]
    missing_skills = state["missing_skills"]
    matched_skills = state["matched_skills"]
    parsed_resume = state["parsed_resume"]

    role = selected_jd["role"]
    required_skills = selected_jd["required_skills"]

    projects = []
    for project in parsed_resume["projects"]:
        projects.append(project["name"])

    prompt = resume_selection_prompt(role,required_skills,matched_skills,missing_skills,projects,selected_jd,parsed_resume)

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    output = response.choices[0].message.content.strip()
    output = output.replace("```json", "").replace("```", "").strip()

    suggestions = json.loads(output)

    return {
        "resume_suggestions": suggestions
    }