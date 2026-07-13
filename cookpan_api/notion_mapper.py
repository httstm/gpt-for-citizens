
def get_title(properties):
    title_prop = properties.get("名前", {}).get("title", [])
    if not title_prop:
        return ""
    return title_prop[0].get("plain_text", "")

def get_category(properties):
    category = properties.get("カテゴリ", {}).get("select")
    if not category:
        return ""
    return category.get("name", "")


def page_to_recipe(page):
    p = page["properties"]

    return {
        "id": page["id"],
        "title": get_title(p),
        "category": get_category(p),
    }