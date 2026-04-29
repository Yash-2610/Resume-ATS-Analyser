def gap_analysis(state):


    resume_skills = set(
        skill.strip().lower()
        for skill in state["parsed_resume"]["skills"]
    )


    jd_skills = set(
        skill.strip().lower()
        for skill in state["selected_jd"]["required_skills"]
    )


    matched_skills = jd_skills.intersection(resume_skills)

    missing_skills = jd_skills.difference(resume_skills)


    total_required = len(jd_skills)

    if total_required == 0:
        match_score = 0.0
    else:
        match_score = round(
            (len(matched_skills) / total_required) * 100,
            2
        )

    print("\n===== GAP ANALYSIS =====")
    print("Matched Skills :", matched_skills)
    print("Missing Skills :", missing_skills)
    print("Match Score    :", match_score)

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "match_score": match_score
    }