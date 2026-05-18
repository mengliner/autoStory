from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project, Character, CharacterRelationship, OutlineNode, Chapter, WorldSetting, Foreshadowing, Candidate
from schemas import (
    ProjectCreate, ProjectUpdate, ProjectOut, ProjectFullState,
    CharacterOut, RelationshipOut, OutlineNodeOut, ChapterOut,
    WorldSettingOut, ForeshadowOut, CandidateOut
)

router = APIRouter()


@router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.updated_at.desc()).all()


@router.post("/projects", response_model=ProjectOut)
def create_project(req: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(title=req.title, synopsis=req.synopsis)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{id}", response_model=ProjectFullState)
def get_project_full_state(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project": project,
        "characters": db.query(Character).filter(Character.project_id == id).all(),
        "relationships": db.query(CharacterRelationship).filter(CharacterRelationship.project_id == id).all(),
        "outline": db.query(OutlineNode).filter(OutlineNode.project_id == id).order_by(OutlineNode.sort_order).all(),
        "chapters": db.query(Chapter).filter(Chapter.project_id == id).all(),
        "settings": db.query(WorldSetting).filter(WorldSetting.project_id == id).all(),
        "foreshadowings": db.query(Foreshadowing).filter(Foreshadowing.project_id == id).all(),
        "candidates": db.query(Candidate).filter(Candidate.project_id == id, Candidate.status == "pending").all()
    }


@router.put("/projects/{id}", response_model=ProjectOut)
def update_project(id: int, req: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if req.title is not None:
        project.title = req.title
    if req.synopsis is not None:
        project.synopsis = req.synopsis
    if req.status is not None:
        project.status = req.status
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{id}")
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"ok": True}


@router.get("/outline/{project_id}", response_model=list[OutlineNodeOut])
def get_outline(project_id: int, db: Session = Depends(get_db)):
    return db.query(OutlineNode).filter(OutlineNode.project_id == project_id).order_by(OutlineNode.sort_order).all()


@router.get("/characters/{project_id}", response_model=list[CharacterOut])
def get_characters(project_id: int, db: Session = Depends(get_db)):
    return db.query(Character).filter(Character.project_id == project_id).all()


@router.get("/relationships/{project_id}", response_model=list[RelationshipOut])
def get_relationships(project_id: int, db: Session = Depends(get_db)):
    return db.query(CharacterRelationship).filter(CharacterRelationship.project_id == project_id).all()


@router.get("/settings/{project_id}", response_model=list[WorldSettingOut])
def get_world_settings(project_id: int, db: Session = Depends(get_db)):
    return db.query(WorldSetting).filter(WorldSetting.project_id == project_id).all()


@router.get("/foreshadowings/{project_id}", response_model=list[ForeshadowOut])
def get_foreshadowings(project_id: int, db: Session = Depends(get_db)):
    return db.query(Foreshadowing).filter(Foreshadowing.project_id == project_id).all()


@router.get("/chapters/{project_id}", response_model=list[ChapterOut])
def get_chapters(project_id: int, db: Session = Depends(get_db)):
    return db.query(Chapter).filter(Chapter.project_id == project_id).all()


@router.get("/chapters/{chapter_id}", response_model=ChapterOut)
def get_chapter_detail(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter
