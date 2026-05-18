TOOLS = [
    {
        "name": "upsert_character",
        "description": "创建或更新角色信息。id 为空时创建，id 有值时更新已有角色。",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "角色ID，更新时必填"},
                "name": {"type": "string", "description": "角色名"},
                "role": {"type": "string", "description": "角色定位：主角/配角/反派"},
                "personality": {"type": "string", "description": "性格描述"},
                "background": {"type": "string", "description": "背景故事"},
                "attributes": {"type": "object", "description": "扩展属性"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "upsert_relationship",
        "description": "添加或修改角色之间的关系",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "关系ID，更新时必填"},
                "char_a_id": {"type": "integer", "description": "角色A的ID"},
                "char_b_id": {"type": "integer", "description": "角色B的ID"},
                "relation_type": {"type": "string", "description": "关系类型：师徒/敌对/恋人/朋友/亲属等"},
                "description": {"type": "string", "description": "关系描述"}
            },
            "required": ["char_a_id", "char_b_id", "relation_type"]
        }
    },
    {
        "name": "upsert_outline",
        "description": "创建或更新大纲节点。parent_id=0 表示根节点。",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "节点ID，更新时必填"},
                "parent_id": {"type": "integer", "description": "父节点ID，0表示根节点"},
                "title": {"type": "string", "description": "节点标题"},
                "summary": {"type": "string", "description": "节点内容摘要"},
                "level": {"type": "string", "enum": ["volume", "chapter", "section"], "description": "层级"},
                "sort_order": {"type": "integer", "description": "排序序号"},
                "status": {"type": "string", "enum": ["outline", "draft", "writing", "done"], "description": "状态"}
            },
            "required": ["title", "level"]
        }
    },
    {
        "name": "reorder_outline",
        "description": "调整大纲节点的父节点或排序位置",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "要移动的节点ID"},
                "new_parent_id": {"type": "integer", "description": "新的父节点ID，0表示根节点"},
                "new_sort_order": {"type": "integer", "description": "新的排序序号"}
            },
            "required": ["id"]
        }
    },
    {
        "name": "upsert_chapter",
        "description": "创建或更新章节正文内容",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "章节ID，更新时必填"},
                "outline_node_id": {"type": "integer", "description": "关联的大纲节点ID"},
                "title": {"type": "string", "description": "章节标题"},
                "content": {"type": "string", "description": "章节正文内容"},
                "status": {"type": "string", "enum": ["draft", "review", "done"], "description": "状态"}
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "upsert_setting",
        "description": "创建或更新世界观设定",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "设定ID，更新时必填"},
                "category": {"type": "string", "description": "分类：地理/历史/魔法/科技/文化/政治/生物/社会"},
                "title": {"type": "string", "description": "设定名称"},
                "description": {"type": "string", "description": "设定描述"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "upsert_foreshadowing",
        "description": "创建或更新伏笔信息。status=resolved 时标记为已回收。",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "伏笔ID，更新时必填"},
                "title": {"type": "string", "description": "伏笔标题"},
                "description": {"type": "string", "description": "伏笔描述"},
                "planted_chapter_id": {"type": "integer", "description": "埋入的章节ID"},
                "resolved_chapter_id": {"type": "integer", "description": "回收的章节ID"},
                "resolved_note": {"type": "string", "description": "回收说明"},
                "status": {"type": "string", "enum": ["planted", "resolved"], "description": "状态"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "save_candidates",
        "description": "暂存多个版本的结构化候选内容，供用户选择。content_type: outline/chapter/character/setting/foreshadowing。payload 为候选数据数组，每项含 version_label 和 data。",
        "input_schema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "会话标识"},
                "content_type": {"type": "string", "enum": ["outline", "chapter", "character", "setting", "foreshadowing"]},
                "payload": {"type": "array", "items": {"type": "object"}, "description": "候选版本数组，每项含 version_label 和 data"}
            },
            "required": ["content_type", "payload"]
        }
    },
    {
        "name": "confirm_candidate",
        "description": "用户确认某个候选版本后，将其数据写入正式表",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {"type": "integer", "description": "要确认的候选ID"}
            },
            "required": ["candidate_id"]
        }
    },
    {
        "name": "discard_candidates",
        "description": "清理未选中的候选版本",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_ids": {"type": "array", "items": {"type": "integer"}, "description": "要丢弃的候选ID列表"}
            },
            "required": ["candidate_ids"]
        }
    }
]
