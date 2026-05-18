from sqlalchemy import Column, Integer, String, Text, JSON, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
import enum


class ProjectStatus(str, enum.Enum):
    planning = "planning"
    writing = "writing"
    done = "done"


class OutlineLevel(str, enum.Enum):
    volume = "volume"
    chapter = "chapter"
    section = "section"


class OutlineStatus(str, enum.Enum):
    outline = "outline"
    draft = "draft"
    writing = "writing"
    done = "done"


class ChapterStatus(str, enum.Enum):
    draft = "draft"
    review = "review"
    done = "done"


class ForeshadowStatus(str, enum.Enum):
    planted = "planted"
    resolved = "resolved"


class CandidateType(str, enum.Enum):
    outline = "outline"
    chapter = "chapter"
    character = "character"
    setting = "setting"
    foreshadowing = "foreshadowing"


class CandidateStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    discarded = "discarded"


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    synopsis = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.planning)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50))
    personality = Column(Text)
    background = Column(Text)
    attributes = Column(JSON)


class CharacterRelationship(Base):
    __tablename__ = "character_relationships"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    char_a_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    char_b_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    relation_type = Column(String(50))
    description = Column(Text)
    char_a = relationship("Character", foreign_keys=[char_a_id])
    char_b = relationship("Character", foreign_keys=[char_b_id])


class OutlineNode(Base):
    __tablename__ = "outline_nodes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("outline_nodes.id"), nullable=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    level = Column(Enum(OutlineLevel), nullable=False)
    sort_order = Column(Integer, default=0)
    status = Column(Enum(OutlineStatus), default=OutlineStatus.outline)
    children = relationship("OutlineNode", backref="parent", remote_side=[id])


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    outline_node_id = Column(Integer, ForeignKey("outline_nodes.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    status = Column(Enum(ChapterStatus), default=ChapterStatus.draft)
    version = Column(Integer, default=1)


class WorldSetting(Base):
    __tablename__ = "world_settings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(String(50))
    title = Column(String(255), nullable=False)
    description = Column(Text)


class Foreshadowing(Base):
    __tablename__ = "foreshadowings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    planted_chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    resolved_chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    resolved_note = Column(Text)
    status = Column(Enum(ForeshadowStatus), default=ForeshadowStatus.planted)


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    session_id = Column(String(100))
    version_label = Column(String(50))
    content_type = Column(Enum(CandidateType), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(Enum(CandidateStatus), default=CandidateStatus.pending)
