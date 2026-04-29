def selection_node(state):

    jd_scores = state["jd_scores"]
    parsed_jds = state["parsed_jds"]

    if not jd_scores:
        return {
            "selected_jd": {},
            "hitl_active": True,
            "hitl_stage": "jd_selection"
        }


    top_job_id = jd_scores[0]["job_id"]

    selected_jd = {}

    for jd in parsed_jds:
        if jd["job_id"] == top_job_id:
            selected_jd = jd
            break



    return {
        "selected_jd": selected_jd,
        "hitl_active": True,
        "hitl_stage": "jd_selection"
    }