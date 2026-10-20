import json
from collections import defaultdict

class SkillGapOptimizer:
    def __init__(self, staff_path="workforce_inventory.json", proj_path="project_requirements.json"):
        with open(staff_path, "r", encoding="utf-8") as f:
            self.staff = json.load(f)
        with open(proj_path, "r", encoding="utf-8") as f:
            self.projects = json.load(f)

    def analyze_gaps(self):
        # 1. Total demand per skill across pipeline projects
        skill_demand = defaultdict(int)
        for p in self.projects:
            for skill, headcount_needed in p["required_skills"].items():
                skill_demand[skill] += headcount_needed

        # 2. Total supply per skill (Qualified: proficiency >= 3)
        skill_supply = defaultdict(int)
        skill_upskillable = defaultdict(int) # proficiency == 2

        for emp in self.staff:
            for skill, level in emp["skills"].items():
                if level >= 3:
                    skill_supply[skill] += 1
                elif level == 2:
                    skill_upskillable[skill] += 1

        # 3. Gap Analysis
        gap_report = []
        all_skills = sorted(list(set(list(skill_demand.keys()) + list(skill_supply.keys()))))
        
        critical_gaps_count = 0
        total_shortfall = 0

        for s in all_skills:
            demand = skill_demand.get(s, 0)
            supply = skill_supply.get(s, 0)
            upskill_pool = skill_upskillable.get(s, 0)
            net_gap = supply - demand # negative means shortage

            status = "HEALTHY"
            recommendation = "Maintain current capacity."
            if net_gap < 0:
                shortage = abs(net_gap)
                total_shortfall += shortage
                if shortage > 3:
                    status = "CRITICAL SHORTAGE"
                    critical_gaps_count += 1
                    recommendation = f"Immediate external hiring needed ({shortage - min(shortage, upskill_pool)} seats) + fast-track bootcamp ({min(shortage, upskill_pool)} candidates)."
                else:
                    status = "MODERATE GAP"
                    recommendation = f"Upskill internal employees from Level 2 pool ({min(shortage, upskill_pool)} available)."
            elif net_gap > 8:
                status = "SURPLUS"
                recommendation = "Reallocate or cross-train surplus staff into higher-demand skill domains."

            gap_report.append({
                "skill": s,
                "demand": demand,
                "supply_qualified": supply,
                "upskillable_candidates": upskill_pool,
                "net_gap": net_gap,
                "status": status,
                "recommendation": recommendation
            })

        gap_report.sort(key=lambda x: x["net_gap"])

        # Project Feasibility Health
        project_feasibility = []
        for p in self.projects:
            total_req = sum(p["required_skills"].values())
            supported_count = 0
            bottleneck_skills = []

            for sk, needed in p["required_skills"].items():
                avail = skill_supply.get(sk, 0)
                if avail >= needed:
                    supported_count += needed
                else:
                    supported_count += avail
                    bottleneck_skills.append(f"{sk} (Need {needed}, Have {avail})")

            coverage_pct = round((supported_count / total_req) * 100, 1)
            project_feasibility.append({
                "name": p["name"],
                "deadline_weeks": p["deadline_weeks"],
                "coverage_pct": coverage_pct,
                "risk_level": "HIGH RISK" if coverage_pct < 70 else "MODERATE" if coverage_pct < 90 else "READY",
                "bottlenecks": bottleneck_skills
            })

        return {
            "summary": {
                "total_headcount": len(self.staff),
                "active_projects": len(self.projects),
                "critical_skill_shortages": critical_gaps_count,
                "total_talent_shortfall": total_shortfall
            },
            "skill_gaps": gap_report,
            "project_health": project_feasibility
        }

if __name__ == "__main__":
    opt = SkillGapOptimizer()
    print(opt.analyze_gaps()["summary"])
