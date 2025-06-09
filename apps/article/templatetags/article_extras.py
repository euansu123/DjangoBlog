from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.filter
def tag_color(tag):
    # 固定的颜色列表
    tag_color = ["bg-blue", "bg-green", "bg-purple", "bg-pink", "bg-teal", "bg-gold", "bg-brown"]
    # articles_tag = [ for index, article in enumerate(articles)]
    # 根据标签名生成固定的颜色索引，这样同一个标签每次都是相同的颜色
    index = hash(tag.name) % len(tag_color)
    return tag_color[index]