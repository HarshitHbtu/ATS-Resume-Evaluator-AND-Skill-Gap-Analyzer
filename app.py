import os
import tempfile
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer, util

from source.parser import extract_resume_text
from source.preprocessing import clean_text, extract_degree, has_portfolio
from source.skill_match import skill_matching
from source.ats_score import calculate_ats_score
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

st.set_page_config(page_title="Resume ATS Score", layout="wide")

st.title("📄 Resume ATS Score Checker")

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume", type="primary"):

    if resume_file is None:
        st.warning("Please upload a resume.")
        st.stop()

    if jd_text.strip() == "":
        st.warning("Please paste Job Description.")
        st.stop()

    # Temporary file handling
    file_ext = "." + resume_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        resume_file.seek(0)
        tmp_file.write(resume_file.read())
        path = tmp_file.name

    try:
        resume_text = extract_resume_text(path)
    finally:
        if os.path.exists(path):
            os.remove(path)

    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)

    # TF-IDF Vectorization & Rescaled Cosine Similarity
   # Semantic Similarity using Sentence Transformers
    emb_resume = model.encode(clean_resume, convert_to_tensor=True)
    emb_jd = model.encode(clean_jd, convert_to_tensor=True)

    raw_cosine = float(util.cos_sim(emb_resume, emb_jd)[0][0])
    cosine_score = max(0.0, min(raw_cosine * 100, 100.0))

    # Non-linear Scaling using Square Root
    cosine_score = np.sqrt(raw_cosine) * 100
    cosine_score = min(cosine_score, 100)

    # Expanded Skill List
    skill_list = [
        "python", "java", "c++", "sql", "git", "github", 
        "machine learning", "deep learning", "numpy", "pandas", 
        "scikit learn", "tensorflow", "pytorch", "data structures", 
        "algorithms", "dbms", "operating systems", "computer networks", 
        "oop", "linux", "aws", "docker", "rest api", "mongodb", "mysql"
    ]

    (
        resume_skills,
        jd_skills,
        matched,
        missing,
        skill_percentage
    ) = skill_matching(
        clean_resume,
        clean_jd,
        skill_list
    )

    resume_degree = extract_degree(resume_text)
    jd_degree = extract_degree(jd_text)

    portfolio = has_portfolio(resume_text)

    result = calculate_ats_score(
        cosine_score,
        skill_percentage,
        resume_degree,
        jd_degree,
        portfolio
    )

    with st.expander("🔍 Debug Information & Preview"):
        st.write(f"**Resume Degree :** {resume_degree}")
        st.write(f"**JD Degree :** {jd_degree}")
        st.write(f"**Raw Cosine Similarity :** {raw_cosine * 100:.2f}%")
        st.write(f"**Scaled Cosine Score :** {cosine_score:.2f}%")
        st.write(f"**Skill Match :** {skill_percentage:.2f}%")
        st.write(f"**Portfolio Found :** {portfolio}")
        st.divider()
        st.write("**Resume Snippet:**", resume_text[:500])
        st.write("**JD Snippet:**", jd_text[:500])

    st.divider()

    st.success(f"🎯 Final ATS Score : {result['ats_score']:.2f}%")

    st.subheader("Score Breakdown")

    st.progress(min(int(result["ats_score"]), 100))

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Cosine Similarity",
            f"{result['cosine_score']:.2f}/30"
        )

        st.metric(
            "Skill Match",
            f"{result['skill_score']:.2f}/50"
        )

    with col2:
        st.metric(
            "Degree Score",
            f"{result['degree_score']}/10"
        )

        st.metric(
            "Portfolio Bonus",
            f"{result['portfolio_score']}/10"
        )

    st.subheader("✅ Matched Skills")

    if matched:
        st.success(", ".join(sorted(matched)))
    else:
        st.warning("No matched skills found.")

    st.subheader("❌ Missing Skills")

    if missing:
        st.error(", ".join(sorted(missing)))
    else:
        st.success("No missing skills detected.")

    st.subheader("📊 Summary")

    if result["ats_score"] >= 80:
        st.success("Excellent Resume! Highly ATS Friendly.")
    elif result["ats_score"] >= 60:
        st.info("Good Resume. A few improvements can increase your ATS score.")
    elif result["ats_score"] >= 40:
        st.warning("Average Resume. Add more relevant skills, projects and keywords.")
    else:
        st.error("Low ATS Score. Tailor your resume according to the Job Description.")

    st.subheader("💡 Suggestions")

    if missing:
        st.write("### Recommended Skills to Add")
        for skill in sorted(missing):
            st.write(f"- {skill}")

    if not portfolio:
        st.warning("Add GitHub, LinkedIn or Portfolio links to gain portfolio bonus.")

    if result["degree_score"] == 0:
        st.warning("Your degree does not satisfy the minimum requirement mentioned in the Job Description.")

    st.info(
        "Tip: Customize your resume for each job by adding the required keywords naturally "
        "in your Projects, Skills and Experience sections."
    )
