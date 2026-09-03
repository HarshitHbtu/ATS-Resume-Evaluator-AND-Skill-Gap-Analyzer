import re

# Skill Synonyms
SKILL_MAP = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "git": ["git"],
    "github": ["github"],
    "machine learning": ["machine learning", "machinelearning", "ml"],
    "deep learning": ["deep learning", "deeplearning", "dl"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "scikit learn": ["scikit learn", "scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "data structures": [
        "data structures",
        "data structure",
        "dsa"
    ],
    "algorithms": [
        "algorithm",
        "algorithms"
    ],
    "dbms": [
        "dbms",
        "database management system"
    ],
    "operating systems": [
        "operating systems",
        "operating system",
        "os"
    ],
    "computer networks": [
        "computer networks",
        "computer network",
        "cn"
    ],
    "oop": [
        "oop",
        "oops",
        "object oriented programming",
        "object-oriented programming"
    ],
    "linux": ["linux"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "rest api": [
        "rest api",
        "restful api",
        "restful apis"
    ],
    "mongodb": ["mongodb", "mongo db"],
    "mysql": ["mysql"]
}


def extract_skills(text, skill_list):
    text = text.lower()
    found_skills = set()

    for skill in skill_list:
        keywords = SKILL_MAP.get(skill.lower(), [skill.lower()])

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                found_skills.add(skill.lower())
                break

    return sorted(list(found_skills))


def skill_matching(resume_text, jd_text, skill_list):

    resume_skills = extract_skills(resume_text, skill_list)

    jd_skills = extract_skills(jd_text, skill_list)

    matched = sorted(
        list(set(resume_skills) & set(jd_skills))
    )

    missing = sorted(
        list(set(jd_skills) - set(resume_skills))
    )

    if len(jd_skills) == 0:
        skill_percentage = 100
    else:
        skill_percentage = (
            len(matched) / len(jd_skills)
        ) * 100

    return (
        resume_skills,
        jd_skills,
        matched,
        missing,
        skill_percentage
    )
