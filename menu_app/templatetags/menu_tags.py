from django import template

from menu_app.models import Menu, MenuItem

register = template.Library()


def build_menu_tree(items, current_path):
    """Вспомогательная функция для постройки дерева"""

    # Словарь всех элементов меню вида ID - элемент
    # Отсюда будем вылавливать нужные элементы, чтобы не делать ещё запросов к БД
    item_dict = {item.id: item for item in items}

    active_item = None  # Активный элемент меню

    # Находим активный элемент меню
    for item in item_dict.values():
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    # Добавляем всех родителей активного элемента
    items_ids = set()  # Множество ID элементов, которые следует отобразить в меню
    # Добавим все корневые элементы во множество
    for item in item_dict.values():
        if item.parent_id is None:
            items_ids.add(item.id)

    def add_parents(item):
        while item and item.id not in items_ids:
            items_ids.add(item.id)
            if item.parent_id:
                item = item_dict.get(item.parent_id)
            else:
                break

    if active_item:
        add_parents(active_item)

    # Добавим детей активного элемента
    for item in item_dict.values():
        if item.parent_id == active_item.id:
            items_ids.add(item.id)

    # Свяжем всех детей и родителей:
    for item in item_dict.values():
        item.children_list = []
    for item in item_dict.values():
        if item.id in items_ids and item.parent_id:
            parent = item_dict.get(item.parent_id)
            if parent and parent.id in items_ids:
                parent.children_list.append(item)

    # Вернем только корневые элементы
    # Все необходимые связи для дальнейшего корректного построения меню уже установлены
    return [
        item
        for item in item_dict.values()
        if item.id in items_ids and item.parent_id is None
    ]


@register.inclusion_tag("menu_app/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """Шаблонный тег draw_menu в Django Templates"""
    request = context["request"]
    current_path = request.path

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {"menu_tree": []}

    all_items = MenuItem.objects.filter(menu=menu).select_related("parent")
    menu_tree = build_menu_tree(all_items, current_path)

    return {"menu_tree": menu_tree, "current_path": current_path}
