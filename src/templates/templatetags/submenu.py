from django.db import connection
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

def fetch_menu_data(search_title):
    with connection.cursor() as cursor:
        cursor.execute('''
            WITH RECURSIVE hierarchy AS (
                SELECT id, title, parent_id, CAST(title AS TEXT) AS path
                FROM menu_app_menuitem
                WHERE title = %s
                UNION ALL
                SELECT m.id, m.title, m.parent_id, CAST(h.path || ' -> ' || m.title AS TEXT)
                FROM menu_app_menuitem m
                JOIN hierarchy h ON m.id = h.parent_id
            ),
            sibling_children AS (
                SELECT
                    h.id,
                    (
                        SELECT GROUP_CONCAT(title, ', ')
                        FROM menu_app_menuitem
                        WHERE parent_id = (
                            SELECT id
                            FROM menu_app_menuitem
                            WHERE title = h.title
                        )
                    ) AS children
                FROM hierarchy h
            )
            SELECT path, children
            FROM hierarchy
            LEFT JOIN sibling_children sc ON hierarchy.id = sc.id
            ORDER BY LENGTH(path) DESC
        ''', [search_title])
        return cursor.fetchall()

def render_submenu(children, menu_item):
    if menu_item in children:
        result = '<ul>'
        for child in children[menu_item]:
            result += f'<li><a href="{reverse("menu_item", kwargs={"menu_item_title": child})}">{child}</a>'
            if child in children:
                result += render_submenu(children, child)
            result += '</li>'
        result += '</ul>'
        return result
    return ''

@register.simple_tag(takes_context=True)
def draw_menu(context):
    request = context['request']
    search_title = request.path.strip('/')

    rows = fetch_menu_data(search_title)

    main_thread = rows[0][0].split(' -> ')
    children = {}

    for thread, node_children in rows[::-1]:
        node = thread.split(' -> ')[-1]
        if node_children:
            children[node] = node_children.split(', ')

    children[''] = main_thread[-1]

    return mark_safe(render_submenu(children, ''))
