import random
import json

SKILLS = [
    "Python / Backend", "Cloud Architecture (AWS/GCP)", "Machine Learning & AI",
    "Data Engineering (SQL/Spark)", "Frontend (React/TypeScript)", "DevOps & CI/CD",
    "Cybersecurity Compliance", "Product Management", "Agile Project Delivery"
]

PROJECTS = [
    {"name": "Project Alpha (Enterprise GenAI Migration)", "deadline_weeks": 8, "required_skills": {"Machine Learning & AI": 6, "Python / Backend": 8, "Cloud Architecture (AWS/GCP)": 5}},
    {"name": "Project Titan (Core FinTech Overhaul)", "deadline_weeks": 12, "required_skills": {"Cloud Architecture (AWS/GCP)": 7, "DevOps & CI/CD": 6, "Cybersecurity Compliance": 5, "Python / Backend": 6}},
    {"name": "Project Velocity (Mobile & Web App V2)", "deadline_weeks": 6, "required_skills": {"Frontend (React/TypeScript)": 8, "Product Management": 3, "Python / Backend": 5}},
    {"name": "Project Lighthouse (Data Lakehouse & BI)", "deadline_weeks": 10, "required_skills": {"Data Engineering (SQL/Spark)": 8, "Machine Learning & AI": 4, "Cloud Architecture (AWS/GCP)": 5}}
]

def generate_skills_data(num_staff=120):
    random.seed(42)
    staff = []
    for i in range(1, num_staff + 1):
        emp_id = f"ENG-{3000 + i}"
        # Each employee has proficiency (1 to 5) across subset of skills
        num_known_skills = random.randint(2, 5)
        assigned_skills = random.sample(SKILLS, num_known_skills)
        skill_matrix = {}
        for s in assigned_skills:
            skill_matrix[s] = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 40, 25, 15])[0]

        staff.append({
            "employee_id": emp_id,
            "department": "Product & Engineering",
            "experience_years": random.randint(1, 15),
            "weekly_availability_hrs": random.choice([20, 30, 40]),
            "skills": skill_matrix
        })

    with open("workforce_inventory.json", "w", encoding="utf-8") as f:
        json.dump(staff, f, indent=2)

    with open("project_requirements.json", "w", encoding="utf-8") as f:
        json.dump(PROJECTS, f, indent=2)

    print(f"Generated workforce skills data for {num_staff} staff across 4 pipeline projects.")

if __name__ == "__main__":
    generate_skills_data()
