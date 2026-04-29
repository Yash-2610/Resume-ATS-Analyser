from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


_embeddings_model = None


def get_embeddings_model():
    global _embeddings_model

    if _embeddings_model is None:
        _embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    return _embeddings_model


def resume_to_text(formatted_resume):
    skills = ", ".join(formatted_resume["skills"])

    projects = []
    for project in formatted_resume["projects"]:
        name = project["name"]
        tech = ", ".join(project["tech_used"])
        projects.append(f"{name} using {tech}")

    return f"Skills: {skills}\nProjects: {' | '.join(projects)}"


def jd_to_text(jd):
    return f"""
    Role: {jd['role']}
    Required Skills: {', '.join(jd['required_skills'])}
    Preferred Skills: {', '.join(jd['good_to_have'])}
    """


def ranking_node(state):

    embeddings_model = get_embeddings_model()

    parsed_resume = state["parsed_resume"]
    parsed_jds = state["parsed_jds"]

    resume_text = resume_to_text(parsed_resume)
    resume_vector = embeddings_model.embed_query(resume_text)

    scores = []

    for jd in parsed_jds:

        jd_text = jd_to_text(jd)
        jd_vector = embeddings_model.embed_query(jd_text)

        similarity = cosine_similarity(
            [resume_vector],
            [jd_vector]
        )[0][0]

        scores.append({
            "job_id": jd["job_id"],
            "role": jd["role"],
            "score": round(similarity * 100, 2)
        })

    scores.sort(key=lambda x: x["score"], reverse=True)

    return {
        "jd_scores": scores
    }