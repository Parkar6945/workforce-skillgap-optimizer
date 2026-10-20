import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from optimizer_engine import SkillGapOptimizer
from data_generator import generate_skills_data

app = FastAPI(title="Workforce Capacity & Skill Gap Optimizer")

if not os.path.exists("workforce_inventory.json"):
    generate_skills_data(120)

optimizer = SkillGapOptimizer()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/skills")
async def get_skills():
    return optimizer.analyze_gaps()

@app.post("/api/recalculate")
async def recalculate():
    generate_skills_data(120)
    global optimizer
    optimizer = SkillGapOptimizer()
    return {"status": "success", "message": "Re-evaluated skill inventory."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)
