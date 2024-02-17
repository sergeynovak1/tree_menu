from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from menu_app.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context):
    request = context['request']
    active_item_url = request.path.strip('/')
    menu_items = MenuItem.objects.filter(title=active_item_url)

    def render_submenu(menu_items):
        result = '<ul>'
        for item in menu_items:
            result += f'<li><a href="{reverse("menu_item", kwargs={"menu_item_title": item.title})}">{item.title}</a>'
            result += '</li>'
        result += '</ul>'
        return result

    if menu_items:
        for item in menu_items:
            return mark_safe(render_submenu([item]))
    return ''
