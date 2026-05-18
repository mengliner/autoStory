from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str
    synopsis: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    synopsis: Optional[str] = None
    status: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    synopsis: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CharacterOut(BaseModel):
    id: int
    project_id: int
    name: str
    role: Optional[str]
    personality: Optional[str]
    background: Optional[str]
    attributes: Optional[Any]

    model_config = {"from_attributes": True}


class RelationshipOut(BaseModel):
    id: int
    project_id: int
    char_a_id: int
    char_b_id: int
    relation_type: Optional[str]
    description: Optional[str]

    model_config = {"from_attributes": True}


class OutlineNodeOut(BaseModel):
    id: int
    project_id: int
    parent_id: Optional[int]
    title: str
    summary: Optional[str]
    level: str
    sort_order: int
    status: str

    model_config = {"from_attributes": True}


class ChapterOut(BaseModel):
    id: int
    project_id: int
    outline_node_id: Optional[int]
    title: str
    content: Optional[str]
    status: str
    version: int

    model_config = {"from_attributes": True}


class WorldSettingOut(BaseModel):
    id: int
    project_id: int
    category: Optional[str]
    title: str
    description: Optional[str]

    model_config = {"from_attributes": True}


class ForeshadowOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    planted_chapter_id: Optional[int]
    resolved_chapter_id: Optional[int]
    resolved_note: Optional[str]
    status: str

    model_config = {"from_attributes": True}


class CandidateOut(BaseModel):
    id: int
    project_id: int
    session_id: Optional[str]
    version_label: Optional[str]
    content_type: str
    payload: Any
    status: str

    model_config = {"from_attributes": True}


class ProjectFullState(BaseModel):
    project: ProjectOut
    characters: list[CharacterOut]
    relationships: list[RelationshipOut]
    outline: list[OutlineNodeOut]
    chapters: list[ChapterOut]
    settings: list[WorldSettingOut]
    foreshadowings: list[ForeshadowOut]
    candidates: list[CandidateOut]


class ChatRequest(BaseModel):
    message: str
