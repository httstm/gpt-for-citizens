def get_title(properties):
    title_prop = properties.get("名前", {}).get("title", [])
    if not title_prop:
        return ""
    return title_prop[0].get("plain_text", "")

def get_rich_text(properties, property_name):
    items = properties.get(property_name, {}).get("rich_text", [])
    if not items:
        return ""

    return "".join(item.get("plain_text", "") for item in items)

def get_select(properties, property_name):
    value = properties.get(property_name, {}).get("select")
    if not value:
        return ""

    return value.get("name", "")

def get_date(properties, property_name):
    value = properties.get(property_name, {}).get("date")
    if not value:
        return ""

    return value.get("start", "")



def page_to_recipe(page):
    p = page["properties"]

    return {
        "id": page["id"],
        "title": get_title(p),
        "category": get_select(p, "カテゴリ"),
        "ingredients": get_rich_text(p, "材料"),
        "instructions": get_rich_text(p, "作り方"),
        "tips": get_rich_text(p, "コツ・ポイント"),
        "description": get_rich_text(p, "説明文"),
        "origin": get_rich_text(p, "レシピの生い立ち"),
        "next_try": get_rich_text(p, "次のtry"),
        "notes": get_rich_text(p, "備考"),
        "yield": get_rich_text(p, "出来上がり量"),
        "recipe_stability": get_select(p, "固定レシピ度"),
        "created_date": get_date(p, "作成日"),
    }