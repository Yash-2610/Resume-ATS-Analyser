# 📄 AI Resume ATS Analyzer

An AI-powered Applicant Tracking System (ATS) Analyzer built using **LangGraph, LLMs, Streamlit, and Embeddings**.

This project helps candidates compare their resume against multiple Job Descriptions (JDs), identify missing skills, generate interview questions, and receive resume improvement suggestions.

---

# 🚀 Live Demo

https://ats-resume-analyser.streamlit.app/

---

# 🔥 Features

## ✅ Resume Parsing
- Upload PDF resume
- Extracts text automatically
- Identifies:
  - Skills
  - Projects
  - Experience

## ✅ Multi Job Description Support
- Add multiple JDs
- Compare against all JDs
- Automatically ranks best matching jobs

## ✅ Smart ATS Scoring
Uses two-layer scoring:

### 1. Semantic Fit Score
Uses embeddings + cosine similarity between resume and JD.

### 2. Skill Match Score
Uses LLM-based skill analysis:
- matched skills
- missing skills
- transferable skills
- weighted importance scoring

## ✅ Human In The Loop (HITL)
User can manually improve results:

- Change selected JD
- Add missing skills
- Change interview difficulty mode

## ✅ Interview Preparation
Generates custom interview questions:

- Easy
- Medium
- Hard
- HR
- Technical

## ✅ Resume Suggestions
AI-generated suggestions to improve resume for selected role.

---

# 🧠 Tech Stack

## Frontend
- Streamlit

## Backend Workflow
- LangGraph

## LLM
- Groq API  
- Llama 3.1 8B Instant

## Embeddings
- HuggingFace all-MiniLM-L6-v2

## Vector Similarity
- Scikit-learn cosine similarity

---

# 📂 Project Structure

```bash
ATS/
│── ui.py
│── main.py
│── state.py
│── parser_node.py
│── embedding_rank_node.py
│── smart_gap_analysis_node.py
│── interview_question_node.py
│── resume_suggestion_node.py
│── hitl_node.py
│── prompts.py
│── selection_node.py
│── llm.py
│── requirements.txt
│── README.md

```

## ⚠️ Note on Results

This application uses Large Language Models (LLMs) and embedding-based similarity to analyze resumes and job descriptions.

While it aims to provide helpful insights, results may not always be perfectly accurate or complete. Factors such as phrasing, context, and model interpretation can affect outcomes.

This tool should be used as a **guidance system**, not as a definitive evaluation.

For best results, users are encouraged to:
- Review suggestions critically
- Use Human-in-the-Loop (HITL) options
- Cross-check important decisions manually