MATERIALS = {
    "45号钢": {
        "name": "45号钢",
        "category": "中碳钢",
        "hardness": "HB170-220",
        "description": "常用中碳结构钢，具有较好的强度和切削加工性能。",
    },
    "铝合金": {
        "name": "铝合金",
        "category": "有色金属",
        "hardness": "较低",
        "description": "密度低，切削加工性能较好，常用于航空、汽车等领域。",
    },
}


def get_material(material_name: str) -> dict:
    """
    查询材料信息。
    """

    material = MATERIALS.get(material_name)

    if material is None:
        return {
            "found": False,
            "message": f"没有找到材料：{material_name}",
        }

    return {
        "found": True,
        "data": material,
    }