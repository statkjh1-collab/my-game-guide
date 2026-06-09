import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import yt_dlp

from database import create_tables, get_db, Chapter, Stage, Agent, Skill, Mob
from seed import seed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()
    seed()

# ───── 냥코대전쟁 API ─────

@app.get("/chapters")
def get_chapters(db: Session = Depends(get_db)):
    chapters = db.query(Chapter).order_by(Chapter.id).all()
    result = []
    for c in chapters:
        result.append({
            "id": c.id,
            "name": c.name,
            "tip": c.tip,
            "stages": [
                {
                    "id": s.id,
                    "name": s.name,
                    "enemies": json.loads(s.enemies) if s.enemies else [],
                    "strategy": s.strategy,
                }
                for s in c.stages
            ]
        })
    return result

@app.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="챕터를 찾을 수 없습니다.")
    return {
        "id": chapter.id,
        "name": chapter.name,
        "tip": chapter.tip,
        "stages": [
            {
                "id": s.id,
                "name": s.name,
                "enemies": json.loads(s.enemies) if s.enemies else [],
                "strategy": s.strategy,
            }
            for s in chapter.stages
        ]
    }

# ───── 발로란트 API ─────

@app.get("/agents")
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).order_by(Agent.id).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "role": a.role,
            "origin": a.origin,
            "description": a.description,
            "difficulty": a.difficulty,
            "tip": a.tip,
            "skills": [
                {"name": sk.name, "type": sk.type, "desc": sk.desc}
                for sk in a.skills
            ]
        }
        for a in agents
    ]

@app.get("/agents/{agent_id}")
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="요원을 찾을 수 없습니다.")
    return {
        "id": agent.id,
        "name": agent.name,
        "role": agent.role,
        "origin": agent.origin,
        "description": agent.description,
        "difficulty": agent.difficulty,
        "tip": agent.tip,
        "skills": [
            {"name": sk.name, "type": sk.type, "desc": sk.desc}
            for sk in agent.skills
        ]
    }

# ───── 마인크래프트 API ─────

@app.get("/mobs")
def get_mobs(db: Session = Depends(get_db)):
    mobs = db.query(Mob).order_by(Mob.id).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "type": m.type,
            "biome": m.biome,
            "description": m.description,
            "drops": json.loads(m.drops) if m.drops else [],
            "tip": m.tip,
            "hp": m.hp,
            "attack": m.attack,
        }
        for m in mobs
    ]

# ───── 유튜브 검색 API ─────

@app.get("/youtube")
def search_youtube(stage: str):
    query = f"냥코대전쟁 레전드 스토리 {stage} 공략"
    ydl_opts = {"quiet": True, "extract_flat": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch5:{query}", download=False)

    videos = result.get("entries", [])
    if not videos:
        return {"error": "검색 결과가 없습니다."}

    sorted_videos = sorted(
        [v for v in videos if v.get("view_count") is not None],
        key=lambda v: v["view_count"],
        reverse=True
    )
    top = sorted_videos[0] if sorted_videos else videos[0]

    return {
        "title": top.get("title"),
        "url": f"https://www.youtube.com/watch?v={top.get('id')}",
        "view_count": top.get("view_count"),
        "channel": top.get("channel") or top.get("uploader"),
        "thumbnail": top.get("thumbnail"),
    }
