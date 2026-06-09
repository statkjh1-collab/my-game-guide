"""
DB 초기 데이터 삽입 스크립트
실행: python seed.py
"""
import json
from database import create_tables, SessionLocal, Chapter, Stage, Agent, Skill, Mob
from data import chapters as chapter_data
from valorant_data import agents as agent_data
from minecraft_data import mobs as mob_data

def seed():
    create_tables()
    db = SessionLocal()

    # 이미 데이터가 있으면 스킵
    if db.query(Chapter).count() > 0:
        print("이미 냥코 데이터가 있습니다. 스킵합니다.")
    else:
        print("냥코대전쟁 데이터 삽입 중...")
        for c in chapter_data:
            chapter = Chapter(name=c["name"], tip=c.get("tip", ""))
            db.add(chapter)
            db.flush()
            for s in c["stages"]:
                stage = Stage(
                    chapter_id=chapter.id,
                    name=s["name"],
                    enemies=json.dumps(s["enemies"], ensure_ascii=False),
                    strategy=s.get("strategy", "")
                )
                db.add(stage)
        db.commit()
        print(f"  → {db.query(Chapter).count()}개 챕터, {db.query(Stage).count()}개 스테이지 삽입 완료")

    if db.query(Agent).count() > 0:
        print("이미 발로란트 데이터가 있습니다. 스킵합니다.")
    else:
        print("발로란트 데이터 삽입 중...")
        for a in agent_data:
            agent = Agent(
                name=a["name"],
                role=a["role"],
                origin=a["origin"],
                description=a["description"],
                difficulty=a["difficulty"],
                tip=a["tip"]
            )
            db.add(agent)
            db.flush()
            for sk in a["skills"]:
                skill = Skill(
                    agent_id=agent.id,
                    name=sk["name"],
                    type=sk["type"],
                    desc=sk["desc"]
                )
                db.add(skill)
        db.commit()
        print(f"  → {db.query(Agent).count()}명 요원 삽입 완료")

    if db.query(Mob).count() > 0:
        print("이미 마인크래프트 데이터가 있습니다. 스킵합니다.")
    else:
        print("마인크래프트 데이터 삽입 중...")
        for m in mob_data:
            mob = Mob(
                name=m["name"],
                type=m["type"],
                biome=m["biome"],
                description=m["description"],
                drops=json.dumps(m["drops"], ensure_ascii=False),
                tip=m["tip"],
                hp=m["hp"],
                attack=m["attack"],
            )
            db.add(mob)
        db.commit()
        print(f"  {db.query(Mob).count()}개 몹 삽입 완료")

    db.close()
    print("시드 완료!")

if __name__ == "__main__":
    seed()
