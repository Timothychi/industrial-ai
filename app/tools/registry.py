from app.tools.material import get_material
from app.tools.knowledge import search_knowledge


TOOLS = {
    "get_material": get_material,
    "search_knowledge": search_knowledge,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_material",
            "description": "查询工业材料的基本信息，例如材料类别、硬度和材料描述。",
            "parameters": {
                "type": "object",
                "properties": {
                    "material_name": {
                        "type": "string",
                        "description": "材料名称，例如45号钢、铝合金",
                    }
                },
                "required": ["material_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "搜索工业制造和加工工艺相关知识。当用户询问工艺、加工方法、注意事项、工艺参数时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要搜索的工业工艺知识。",
                    }
                },
                "required": ["query"],
            },
        },
    },
]