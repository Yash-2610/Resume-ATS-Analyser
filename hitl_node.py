
def select_jd_node(state, selected_job_id):

    for jd in state["parsed_jds"]:
        if jd["job_id"] == selected_job_id:

            return {
                "selected_jd": jd,
                "hitl_active": False,
                "hitl_stage": "gap_review"
            }

    return {}

def add_skills_node(state, skills):

    parsed_resume = state["parsed_resume"]

    current = set(
        s.strip().lower()
        for s in parsed_resume["skills"]
    )

    for skill in skills:
        if skill:
            skill = skill.strip().lower()
            current.add(skill)

    parsed_resume["skills"] = list(current)

    return {
        "parsed_resume": parsed_resume,
        "hitl_active": False,
        "hitl_stage": "gap_review"
    }


def interview_mode_node(state, mode):

    return {
        "user_input": mode,
        "hitl_active": False,
        "hitl_stage": "interview"
    }