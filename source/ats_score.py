def calculate_ats_score(score,
                        skill_percentage,
                        resume_degree,
                        jd_degree,
                        portfolio):

    # Cosine Similarity (30 Marks)
    cosine_score = (score / 100) * 30

    # Skill Match (50 Marks)
    skill_score = (skill_percentage / 100) * 50

    # Degree Match (10 Marks)
    degree_rank = {
        "high school": 0,
        "diploma": 1,
        "bachelors": 2,
        "masters": 3,
        "phd": 4
    }

    if degree_rank[resume_degree] >= degree_rank[jd_degree]:
        degree_score = 10
    else:
        degree_score = 0

    # Portfolio Bonus (10 Marks)
    portfolio_score = 10 if portfolio else 0

    # Final Score
    final_score = (
        cosine_score +
        skill_score +
        degree_score +
        portfolio_score
    )

    return {
        "ats_score": final_score,
        "cosine_score": cosine_score,
        "skill_score": skill_score,
        "degree_score": degree_score,
        "portfolio_score": portfolio_score
    }
