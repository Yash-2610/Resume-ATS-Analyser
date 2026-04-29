from langgraph.graph import StateGraph, START, END
from state import GraphState
from parser_node import extract_text, formatted_resume, formatted_jds
from embedding_rank_node import ranking_node
from selecion_node import selection_node
from smart_gap_analysis_node import smart_gap_analysis
from interview_question_node import interview_questions
from resume_suggestion_node import resume_suggestions
from hilt_node import add_skills_node, select_jd_node

graph = StateGraph(GraphState)

graph.add_node("resume_parser_node", formatted_resume)
graph.add_node("jd_parser_node", formatted_jds)
graph.add_node("ranking_node", ranking_node)
graph.add_node("selection_node", selection_node)
graph.add_node("gap_analysis_node", smart_gap_analysis)
graph.add_node("interview_question_node", interview_questions)
graph.add_node("resume_suggestions_node", resume_suggestions)

graph.add_edge(START, "resume_parser_node")
graph.add_edge(START, "jd_parser_node")
graph.add_edge("resume_parser_node", "ranking_node")
graph.add_edge("jd_parser_node", "ranking_node")
graph.add_edge("ranking_node", "selection_node")
graph.add_edge("selection_node", "gap_analysis_node")
graph.add_edge("gap_analysis_node", "interview_question_node")
graph.add_edge("gap_analysis_node", "resume_suggestions_node")
graph.add_edge("interview_question_node", END)
graph.add_edge("resume_suggestions_node", END)

app = graph.compile()



if __name__ == "__main__":

    resume_text = extract_text("Yash-Resume.pdf")

    raw_jds = [
        "Machine Learning Engineer Required Skills Python SQL TensorFlow Docker",
        "Data Scientist Required Skills Python Pandas Statistics Machine Learning",
        "Machine learning engineer required skills python rag keras langchain tensorflow scikit-learn"
    ]

    initial_state = {
        "raw_resume": resume_text,
        "raw_jds": raw_jds,
        "parsed_resume": {},
        "parsed_jds": []
    }

    result = app.invoke(initial_state)

    print(result)

    state = result

    while True:

        print("\n1 Change JD")
        print("2 Add Skills")
        print("3 Exit")

        choice = input("Choose: ")

        if choice == "1":

            jd_id = input("Enter jd id: ")

            state.update(select_jd_node(state, jd_id))
            state.update(smart_gap_analysis(state))
            state.update(interview_questions(state))
            state.update(resume_suggestions(state))

        elif choice == "2":

            skills = input("Enter skills: ").split(",")

            state.update(add_skills_node(state, skills))
            state.update(smart_gap_analysis(state))
            state.update(interview_questions(state))
            state.update(resume_suggestions(state))

        elif choice == "3":
            break