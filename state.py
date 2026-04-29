from typing import TypedDict, List, Dict

class GraphState(TypedDict):

    raw_resume: str
    raw_jds: List[str]

    parsed_resume: Dict
    parsed_jds: List[Dict]

    jd_scores: List[Dict]
    selected_jd: Dict

    matched_skills: List[str]
    missing_skills: List[str]
    match_score: float

    related_skills: List[str]
    skill_weights: Dict[str, int]

    hitl_active: bool
    hitl_stage: str
    user_input: str

    interview_questions: List[Dict]
    interview_mode: str
    resume_suggestions: List[str]