def resume_embedding(resume_text):
    return f"""
   You are an expert resume parser.

TASK:
Read the resume text and extract information ONLY into the exact JSON format below.

STRICT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanation text.
4. Use only information explicitly present in the resume.
5. Extract skills even if mentioned inside projects or experience.
6. Normalize abbreviations:
   ML = Machine Learning
   NLP = Natural Language Processing
   DL = Deep Learning
   AI = Artificial Intelligence
7. Remove duplicates.
8. If no projects exist, return empty list [].
9. If no experience exists, return empty list [].
10. Keep skill names clean and concise.

RETURN THIS EXACT JSON SHAPE:

{
  "skills": [],
  "projects": [
    {
      "name": "",
      "tech_used": []
    }
  ],
  "experience": [
    {
      "role": "",
      "tech_used": []
    }
  ]
}

RESUME TEXT:
{resume_text}
"""
    

def jd_embedding(jd_text):
    return f"""
   You are an expert job description parser.

TASK:
Read the job descriptions and convert them ONLY into the exact JSON array format below.

STRICT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanation text.
4. One object per job description.
5. Assign IDs sequentially:
   jd_1, jd_2, jd_3 ...
6. Extract role/title clearly.
7. Put mandatory requirements into required_skills.
8. Put preferred / nice-to-have / bonus skills into good_to_have.
9. Normalize abbreviations:
   ML = Machine Learning
   NLP = Natural Language Processing
   AI = Artificial Intelligence
10. Remove duplicates.
11. If no preferred skills exist, return empty list [].

RETURN THIS EXACT JSON SHAPE:

[
  {
    "job_id": "",
    "role": "",
    "required_skills": [],
    "good_to_have": []
  }
]

JOB DESCRIPTIONS:
{jd_text}   
    """
def resume_embedding(resume_text):
    return f"""
You are an expert resume parser.

TASK:
Read the resume text and extract information ONLY into the exact JSON format below.

STRICT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanation text.
4. Use only information explicitly present in the resume.
5. Extract skills even if mentioned inside projects or experience.
6. Normalize abbreviations:
   ML = Machine Learning
   NLP = Natural Language Processing
   DL = Deep Learning
   AI = Artificial Intelligence
7. Remove duplicates.
8. If no projects exist, return empty list [].
9. If no experience exists, return empty list [].
10. Keep skill names clean and concise.

RETURN THIS EXACT JSON SHAPE:

{{
  "skills": [],
  "projects": [
    {{
      "name": "",
      "tech_used": []
    }}
  ],
  "experience": [
    {{
      "role": "",
      "tech_used": []
    }}
  ]
}}

RESUME TEXT:
{resume_text}
"""


def jd_embedding(jd_text):
    return f"""
You are an expert job description parser.

TASK:
Read the job descriptions and convert them ONLY into the exact JSON array format below.

STRICT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanation text.
4. One object per job description.
5. Assign IDs sequentially:
   jd_1, jd_2, jd_3 ...
6. Extract role/title clearly.
7. Put mandatory requirements into required_skills.
8. Put preferred / nice-to-have / bonus skills into good_to_have.
9. Normalize abbreviations:
   ML = Machine Learning
   NLP = Natural Language Processing
   AI = Artificial Intelligence
10. Remove duplicates.
11. If no preferred skills exist, return empty list [].

RETURN THIS EXACT JSON SHAPE:

[
  {{
    "job_id": "",
    "role": "",
    "required_skills": [],
    "good_to_have": []
  }}
]

JOB DESCRIPTIONS:
{jd_text}
"""


def interview_question(role,required_skills,matched_skills,missing_skills,projects,mode):
    return f"""
You are an expert technical interviewer.

Generate 8 interview questions for a candidate applying for:

ROLE: {role}

Difficulty: {mode}

Required Skills:
{required_skills}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Candidate Projects:
{projects}

RULES:
1. Return ONLY JSON list
2. No markdown
3. Include mix of Easy, Medium, Hard
4. Focus on role skills
5. Ask some questions on missing skills
6. Ask some project-based questions

FORMAT:

[
 {{
   "question": "",
   "topic": "",
   "difficulty": ""
 }}
]
"""

def resume_selection_prompt(role,required_skills,matched_skills,missing_skills,projects,parsed_resume,selected_jd):
    
    return f"""
You are an expert resume coach.

Candidate is applying for:

ROLE: {role}

Required Skills:
{required_skills}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Candidate Projects:
{projects}

Current Resume:
{parsed_resume}
Given Job Description:
{selected_jd}

TASK:
Give 7 concise actionable resume improvement suggestions.

RULES:
1. Return ONLY JSON list
2. No markdown
3. Practical suggestions only
4. Focus on improving ATS score + recruiter appeal
5. Mention projects when useful
6.Emphasise more on project whenever possible

FORMAT:

[
  "Add quantified impact to project bullets",
  "Include Docker if you know it",
  "..."
]
"""
def smart_gap_analysis_prompt(resume_skills, projects, selected_jd):
    return f"""
You are a strict JSON API for an ATS system.

Your ONLY job is to compare a candidate resume with a selected job description.

You MUST return EXACTLY ONE valid JSON object.
You MUST return NO explanation.
You MUST return NO markdown.
You MUST return NO code fences.
You MUST return NO text before JSON.
You MUST return NO text after JSON.

--------------------------------------------------
INPUT DATA
--------------------------------------------------

Candidate Skills:
{resume_skills}

Projects:
{projects}

Selected Job Description:
{selected_jd}

--------------------------------------------------
TASK
--------------------------------------------------

Compare candidate profile vs selected job description.

1. Detect abbreviations, aliases, shorthand, synonyms.

Examples:
ML = Machine Learning
DL = Deep Learning
NLP = Natural Language Processing
CV = Computer Vision
TF = TensorFlow
sklearn = Scikit-learn
RAG Pipeline = RAG
LLM Apps = LLM

2. Find skills clearly present in both candidate and JD.

3. Find required JD skills missing in candidate.

4. Find related / transferable skills candidate has.

5. Assign importance weights ONLY for JD skills:
5 = critical
3 = useful
1 = minor

--------------------------------------------------
STRICT OUTPUT RULES
--------------------------------------------------

1. Output MUST be EXACTLY one JSON object.

2. Arrays MUST contain ONLY strings.

3. DO NOT place objects inside arrays.

WRONG:
"matched_skills": [{{"skill":"python"}}]

RIGHT:
"matched_skills": ["python"]

4. skill_weights MUST be a flat dictionary:
string key -> integer value

WRONG:
"skill_weights": {{"python":"high"}}

RIGHT:
"skill_weights": {{"python":5}}

5. Convert all skill names to lowercase.

6. Remove duplicates.

7. Use short clean skill names only.

8. If no value exists, return empty list [] or empty object {{}}.

9. Never invent fake skills not implied by JD or resume.

10. Return only this schema.

--------------------------------------------------
REQUIRED JSON SCHEMA
--------------------------------------------------

{{
  "matched_skills": [
    "string"
  ],
  "missing_skills": [
    "string"
  ],
  "related_skills": [
    "string"
  ],
  "skill_weights": {{
    "skill_name": 5
  }}
}}

--------------------------------------------------
FINAL REMINDER
--------------------------------------------------

Return ONLY raw JSON.
No markdown.
No explanation.
No notes.
No extra characters.
"""