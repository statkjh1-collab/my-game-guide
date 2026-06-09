from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

DATABASE_URL = "sqlite:///./gamedb.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# ───── 냥코대전쟁 ─────
class Chapter(Base):
    __tablename__ = "chapters"
    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String, nullable=False)
    tip     = Column(Text)
    stages  = relationship("Stage", back_populates="chapter", cascade="all, delete-orphan")

class Stage(Base):
    __tablename__ = "stages"
    id         = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    name       = Column(String, nullable=False)
    enemies    = Column(Text)   # JSON 문자열로 저장
    strategy   = Column(Text)
    chapter    = relationship("Chapter", back_populates="stages")

# ───── 발로란트 ─────
class Agent(Base):
    __tablename__ = "agents"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    role        = Column(String)
    origin      = Column(String)
    description = Column(Text)
    difficulty  = Column(String)
    tip         = Column(Text)
    skills      = relationship("Skill", back_populates="agent", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"
    id       = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name     = Column(String)
    type     = Column(String)
    desc     = Column(Text)
    agent    = relationship("Agent", back_populates="skills")

# ───── 마인크래프트 ─────
class Mob(Base):
    __tablename__ = "mobs"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    type        = Column(String)   # 평화적 / 중립적 / 적대적 / 보스
    biome       = Column(String)
    description = Column(Text)
    drops       = Column(Text)     # JSON 문자열
    tip         = Column(Text)
    hp          = Column(Integer)
    attack      = Column(Integer)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
