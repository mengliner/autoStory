from sqlalchemy.orm import Session
from models import (
    Project, Character, CharacterRelationship, OutlineNode, Chapter,
    WorldSetting, Foreshadowing, Candidate, OutlineLevel, OutlineStatus,
    ChapterStatus, ForeshadowStatus, CandidateType, CandidateStatus
)
from schemas import OutlineNodeOut, CharacterOut, RelationshipOut
import json


def execute_tool(tool_name: str, tool_input: dict, project_id: int, db: Session) -> dict:
    """执行 AI 工具调用，返回 {success: bool, data: Any, table: str, action: str}"""

    if tool_name == "upsert_character":
        return _upsert_character(tool_input, project_id, db)
    elif tool_name == "upsert_relationship":
        return _upsert_relationship(tool_input, project_id, db)
    elif tool_name == "upsert_outline":
        return _upsert_outline(tool_input, project_id, db)
    elif tool_name == "reorder_outline":
        return _reorder_outline(tool_input, project_id, db)
    elif tool_name == "upsert_chapter":
        return _upsert_chapter(tool_input, project_id, db)
    elif tool_name == "upsert_setting":
        return _upsert_setting(tool_input, project_id, db)
    elif tool_name == "upsert_foreshadowing":
        return _upsert_foreshadowing(tool_input, project_id, db)
    elif tool_name == "save_candidates":
        return _save_candidates(tool_input, project_id, db)
    elif tool_name == "confirm_candidate":
        return _confirm_candidate(tool_input, project_id, db)
    elif tool_name == "discard_candidates":
        return _discard_candidates(tool_input, db)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def _upsert_character(input: dict, project_id: int, db: Session) -> dict:
    char_id = input.get("id")
    if char_id:
        char = db.query(Character).filter(Character.id == char_id, Character.project_id == project_id).first()
        if not char:
            return {"success": False, "data": None, "table": "characters", "action": "error", "message": "Character not found"}
        for key in ["name", "role", "personality", "background"]:
            if key in input:
                setattr(char, key, input[key])
        if "attributes" in input:
            char.attributes = input["attributes"]
        action = "update"
    else:
        char = Character(project_id=project_id, **{k: v for k, v in input.items() if k in ["name", "role", "personality", "background", "attributes"]})
        db.add(char)
        action = "create"
    db.commit()
    db.refresh(char)
    return {"success": True, "data": _char_to_dict(char), "table": "characters", "action": action}


def _upsert_relationship(input: dict, project_id: int, db: Session) -> dict:
    rel_id = input.get("id")
    if rel_id:
        rel = db.query(CharacterRelationship).filter(CharacterRelationship.id == rel_id, CharacterRelationship.project_id == project_id).first()
        if not rel:
            return {"success": False, "data": None, "table": "character_relationships", "action": "error"}
        for key in ["char_a_id", "char_b_id", "relation_type", "description"]:
            if key in input:
                setattr(rel, key, input[key])
        action = "update"
    else:
        rel = CharacterRelationship(project_id=project_id, **{k: v for k, v in input.items() if k in ["char_a_id", "char_b_id", "relation_type", "description"]})
        db.add(rel)
        action = "create"
    db.commit()
    db.refresh(rel)
    return {"success": True, "data": {"id": rel.id, "project_id": rel.project_id, "char_a_id": rel.char_a_id, "char_b_id": rel.char_b_id, "relation_type": rel.relation_type, "description": rel.description}, "table": "character_relationships", "action": action}


def _upsert_outline(input: dict, project_id: int, db: Session) -> dict:
    node_id = input.get("id")
    parent_id = input.get("parent_id") if input.get("parent_id") and input["parent_id"] != 0 else None
    if node_id:
        node = db.query(OutlineNode).filter(OutlineNode.id == node_id, OutlineNode.project_id == project_id).first()
        if not node:
            return {"success": False, "data": None, "table": "outline_nodes", "action": "error"}
        for key in ["title", "summary", "status"]:
            if key in input:
                setattr(node, key, input[key])
        if "level" in input:
            node.level = OutlineLevel(input["level"])
        if "sort_order" in input:
            node.sort_order = input["sort_order"]
        if "parent_id" in input:
            node.parent_id = parent_id
        action = "update"
    else:
        node = OutlineNode(
            project_id=project_id,
            parent_id=parent_id,
            title=input["title"],
            summary=input.get("summary", ""),
            level=OutlineLevel(input["level"]),
            sort_order=input.get("sort_order", 0),
            status=OutlineStatus(input.get("status", "outline"))
        )
        db.add(node)
        action = "create"
    db.commit()
    db.refresh(node)
    return {"success": True, "data": _outline_to_dict(node), "table": "outline_nodes", "action": action}


def _reorder_outline(input: dict, project_id: int, db: Session) -> dict:
    node = db.query(OutlineNode).filter(OutlineNode.id == input["id"], OutlineNode.project_id == project_id).first()
    if not node:
        return {"success": False, "data": None, "table": "outline_nodes", "action": "error"}
    if "new_parent_id" in input:
        node.parent_id = input["new_parent_id"] if input["new_parent_id"] != 0 else None
    if "new_sort_order" in input:
        node.sort_order = input["new_sort_order"]
    db.commit()
    db.refresh(node)
    return {"success": True, "data": _outline_to_dict(node), "table": "outline_nodes", "action": "update"}


def _upsert_chapter(input: dict, project_id: int, db: Session) -> dict:
    chap_id = input.get("id")
    if chap_id:
        chap = db.query(Chapter).filter(Chapter.id == chap_id, Chapter.project_id == project_id).first()
        if not chap:
            return {"success": False, "data": None, "table": "chapters", "action": "error"}
        for key in ["title", "content", "status", "outline_node_id"]:
            if key in input:
                setattr(chap, key, input[key])
        chap.version += 1
        action = "update"
    else:
        chap = Chapter(project_id=project_id, **{k: v for k, v in input.items() if k in ["title", "content", "status", "outline_node_id"]})
        db.add(chap)
        action = "create"
    db.commit()
    db.refresh(chap)
    return {"success": True, "data": {"id": chap.id, "project_id": chap.project_id, "outline_node_id": chap.outline_node_id, "title": chap.title, "content": chap.content, "status": chap.status.value, "version": chap.version}, "table": "chapters", "action": action}


def _upsert_setting(input: dict, project_id: int, db: Session) -> dict:
    sid = input.get("id")
    if sid:
        s = db.query(WorldSetting).filter(WorldSetting.id == sid, WorldSetting.project_id == project_id).first()
        if not s:
            return {"success": False, "data": None, "table": "world_settings", "action": "error"}
        for key in ["category", "title", "description"]:
            if key in input:
                setattr(s, key, input[key])
        action = "update"
    else:
        s = WorldSetting(project_id=project_id, **{k: v for k, v in input.items() if k in ["category", "title", "description"]})
        db.add(s)
        action = "create"
    db.commit()
    db.refresh(s)
    return {"success": True, "data": {"id": s.id, "project_id": s.project_id, "category": s.category, "title": s.title, "description": s.description}, "table": "world_settings", "action": action}


def _upsert_foreshadowing(input: dict, project_id: int, db: Session) -> dict:
    fid = input.get("id")
    if fid:
        f = db.query(Foreshadowing).filter(Foreshadowing.id == fid, Foreshadowing.project_id == project_id).first()
        if not f:
            return {"success": False, "data": None, "table": "foreshadowings", "action": "error"}
        for key in ["title", "description", "planted_chapter_id", "resolved_chapter_id", "resolved_note"]:
            if key in input:
                setattr(f, key, input[key])
        if "status" in input:
            f.status = ForeshadowStatus(input["status"])
        action = "update"
    else:
        f = Foreshadowing(project_id=project_id, **{k: v for k, v in input.items() if k in ["title", "description", "planted_chapter_id", "status"]})
        db.add(f)
        action = "create"
    db.commit()
    db.refresh(f)
    return {"success": True, "data": {"id": f.id, "project_id": f.project_id, "title": f.title, "description": f.description, "planted_chapter_id": f.planted_chapter_id, "resolved_chapter_id": f.resolved_chapter_id, "resolved_note": f.resolved_note, "status": f.status.value}, "table": "foreshadowings", "action": action}


def _save_candidates(input: dict, project_id: int, db: Session) -> dict:
    payload = input["payload"]
    content_type = CandidateType(input["content_type"])
    session_id = input.get("session_id", "")
    candidates = []
    for item in payload:
        c = Candidate(
            project_id=project_id,
            session_id=session_id,
            version_label=item.get("version_label", ""),
            content_type=content_type,
            payload=item.get("data", item),
            status=CandidateStatus.pending
        )
        db.add(c)
        db.commit()
        db.refresh(c)
        candidates.append({"id": c.id, "version_label": c.version_label, "content_type": c.content_type.value, "payload": c.payload, "status": c.status.value})
    return {"success": True, "data": candidates, "table": "candidates", "action": "create"}


def _confirm_candidate(input: dict, project_id: int, db: Session) -> dict:
    c = db.query(Candidate).filter(Candidate.id == input["candidate_id"], Candidate.project_id == project_id).first()
    if not c:
        return {"success": False, "data": None, "table": "candidates", "action": "error"}
    payload = c.payload
    content_type = c.content_type

    if content_type == CandidateType.character:
        if isinstance(payload, list):
            for item in payload:
                _upsert_character(item, project_id, db)
        else:
            _upsert_character(payload, project_id, db)
    elif content_type == CandidateType.outline:
        if isinstance(payload, list):
            for item in payload:
                _upsert_outline(item, project_id, db)
        else:
            _upsert_outline(payload, project_id, db)
    elif content_type == CandidateType.chapter:
        if isinstance(payload, list):
            for item in payload:
                _upsert_chapter(item, project_id, db)
        else:
            _upsert_chapter(payload, project_id, db)
    elif content_type == CandidateType.setting:
        if isinstance(payload, list):
            for item in payload:
                _upsert_setting(item, project_id, db)
        else:
            _upsert_setting(payload, project_id, db)
    elif content_type == CandidateType.foreshadowing:
        if isinstance(payload, list):
            for item in payload:
                _upsert_foreshadowing(item, project_id, db)
        else:
            _upsert_foreshadowing(payload, project_id, db)

    c.status = CandidateStatus.confirmed
    db.commit()
    return {"success": True, "data": {"id": c.id, "content_type": c.content_type.value, "status": "confirmed"}, "table": "candidates", "action": "confirm"}


def _discard_candidates(input: dict, db: Session) -> dict:
    ids = input["candidate_ids"]
    db.query(Candidate).filter(Candidate.id.in_(ids)).update({Candidate.status: CandidateStatus.discarded}, synchronize_session=False)
    db.commit()
    return {"success": True, "data": {"discarded_ids": ids}, "table": "candidates", "action": "discard"}


def build_state_summary(project_id: int, db: Session) -> str:
    """构建当前故事状态摘要，用于 system prompt"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return ""

    chars = db.query(Character).filter(Character.project_id == project_id).all()
    rels = db.query(CharacterRelationship).filter(CharacterRelationship.project_id == project_id).all()
    outline = db.query(OutlineNode).filter(OutlineNode.project_id == project_id).order_by(OutlineNode.sort_order).all()
    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).all()
    settings = db.query(WorldSetting).filter(WorldSetting.project_id == project_id).all()
    fores = db.query(Foreshadowing).filter(Foreshadowing.project_id == project_id).all()

    parts = [f"## 项目信息\n- 标题: {project.title}\n- 简介: {project.synopsis or '暂无'}\n- 状态: {project.status.value}"]

    if outline:
        o_lines = ["## 当前大纲"]
        for n in outline:
            indent = "  " * (0 if n.level.value == "volume" else 1 if n.level.value == "chapter" else 2)
            o_lines.append(f"{indent}- [{n.level.value}] {n.title} (id={n.id}, status={n.status.value})")
            if n.summary:
                o_lines.append(f"{indent}  {n.summary[:100]}")
        parts.append("\n".join(o_lines))

    if chars:
        c_lines = ["## 角色列表"]
        for c in chars:
            c_lines.append(f"- {c.name} (id={c.id}, role={c.role}): {c.personality or ''} | {c.background or ''}")
        parts.append("\n".join(c_lines))

    if rels:
        r_lines = ["## 角色关系"]
        for r in rels:
            r_lines.append(f"- {r.char_a.name if r.char_a else '?'} → {r.char_b.name if r.char_b else '?'}: {r.relation_type} ({r.description or ''})")
        parts.append("\n".join(r_lines))

    if settings:
        s_lines = ["## 世界观设定"]
        for s in settings:
            s_lines.append(f"- [{s.category}] {s.title}: {s.description or ''}")
        parts.append("\n".join(s_lines))

    if fores:
        f_lines = ["## 伏笔"]
        for f in fores:
            f_lines.append(f"- {f.title} (status={f.status.value}): {f.description or ''}")
        parts.append("\n".join(f_lines))

    if chapters:
        ch_lines = ["## 已完成章节"]
        for ch in chapters:
            if ch.status.value == "done":
                ch_lines.append(f"- {ch.title} (v{ch.version})")
        if len(ch_lines) > 1:
            parts.append("\n".join(ch_lines))

    return "\n\n".join(parts)


def _char_to_dict(c: Character) -> dict:
    return {"id": c.id, "project_id": c.project_id, "name": c.name, "role": c.role, "personality": c.personality, "background": c.background, "attributes": c.attributes}


def _outline_to_dict(n: OutlineNode) -> dict:
    return {"id": n.id, "project_id": n.project_id, "parent_id": n.parent_id, "title": n.title, "summary": n.summary, "level": n.level.value, "sort_order": n.sort_order, "status": n.status.value}
