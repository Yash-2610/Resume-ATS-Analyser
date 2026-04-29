import streamlit as st
import tempfile

from main import app
from parser_node import extract_text
from hitl_node import select_jd_node, add_skills_node, interview_mode_node
from smart_gap_analysis_node import smart_gap_analysis
from interview_question_node import interview_questions
from resume_suggestion_node import resume_suggestions


st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    layout="wide"
)

st.title("📄 AI Resume ATS Analyzer")
st.caption("Demo project — limited usage")


MAX_SESSION_REQUESTS = 5
GLOBAL_LIMIT = 70



def read_usage():
    try:
        with open("usage.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def update_usage():
    count = read_usage() + 1
    with open("usage.txt", "w") as f:
        f.write(str(count))
    return count



if "state" not in st.session_state:
    st.session_state.state = None

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0


st.sidebar.info(
    "AI based analysis may not always be fully accurate. Use as guidance."
)
st.sidebar.header("Inputs")

st.sidebar.write(
    f"Session Usage: {st.session_state.usage_count}/{MAX_SESSION_REQUESTS}"
)
st.sidebar.write(
    f"Global Usage: {read_usage()}/{GLOBAL_LIMIT}"
)

dev_mode=False
if dev_mode:

    if st.sidebar.button("🔄 Reset Session Usage"):
        st.session_state.usage_count = 0
        st.success("Session usage reset!")

    if st.sidebar.button("🔄 Reset Global Usage"):
        with open("usage.txt", "w") as f:
            f.write("0")
        st.success("Global usage reset!")


resume_file = st.sidebar.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

jd_count = st.sidebar.number_input(
    "Number of JDs",
    min_value=1,
    max_value=10,
    value=2
)

raw_jds = []

for i in range(jd_count):
    jd = st.sidebar.text_area(
        f"JD {i+1}",
        key=f"jd_{i}"
    )
    if jd.strip():
        raw_jds.append(jd)


run_btn = st.sidebar.button("🚀 Run Analysis")


if run_btn:

    
    if st.session_state.usage_count >= MAX_SESSION_REQUESTS:
        st.error("Session limit reached.")
        st.stop()

    if read_usage() >= GLOBAL_LIMIT:
        st.error("Global usage limit reached.")
        st.stop()

    
    if resume_file is None:
        st.error("Upload resume.")
        st.stop()

    if len(raw_jds) == 0:
        st.error("Enter at least one JD.")
        st.stop()

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        temp_path = tmp.name

    resume_text = extract_text(temp_path)

    initial_state = {
        "raw_resume": resume_text,
        "raw_jds": raw_jds,
        "parsed_resume": {},
        "parsed_jds": []
    }

    result = app.invoke(initial_state)

    st.session_state.state = result

    st.session_state.usage_count += 1
    update_usage()



if st.session_state.state:

    state = st.session_state.state

    st.divider()
    st.subheader("📌 Recommended Job")

    st.success(state["selected_jd"]["role"])

    st.metric("Match Score", f'{state["match_score"]}%')

   
    st.subheader("Ranked Jobs")

    for jd in state["jd_scores"]:
        st.write(
            f'{jd["job_id"]} | {jd["role"]} | Score: {jd["score"]}%'
        )

  
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matched Skills")
        for skill in state["matched_skills"]:
            st.write(f"- {skill}")

    with col2:
        st.subheader("Missing Skills")
        for skill in state["missing_skills"]:
            st.write(f"- {skill}")

   
    st.subheader("🎯 Interview Questions")

    for q in state["interview_questions"]:
        with st.expander(f'{q["difficulty"]} | {q["topic"]}'):
            st.write(q["question"])

    
    st.subheader("📝 Resume Suggestions")

    for tip in state["resume_suggestions"]:
        st.write(f"- {tip}")


    st.divider()
    st.subheader("Modify")

   
    options = [jd["job_id"] for jd in state["parsed_jds"]]

    selected_option = st.selectbox("Change JD", options)

    if st.button("Apply JD Change"):
        state.update(select_jd_node(state, selected_option))
        state.update(smart_gap_analysis(state))
        state.update(interview_questions(state))
        state.update(resume_suggestions(state))

        st.session_state.state = state
        st.rerun()

    
    skills_text = st.text_input("Add Skills")

    if st.button("Add Skills"):
        skills = skills_text.split(",")

        state.update(add_skills_node(state, skills))
        state.update(smart_gap_analysis(state))
        state.update(interview_questions(state))
        state.update(resume_suggestions(state))

        st.session_state.state = state
        st.rerun()

    
    mode = st.radio(
        "Interview Mode",
        ["Easy", "Medium", "Hard", "HR", "Technical"]
    )

    if st.button("Update Mode"):
        state.update(interview_mode_node(state, mode))
        state.update(interview_questions(state))

        st.session_state.state = state
        st.rerun()

