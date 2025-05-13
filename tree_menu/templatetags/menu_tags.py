from django import template
from django.urls import resolve
from tree_menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    
    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    
    menu_tree = []
    items_dict = {}
    
    for item in items:
        items_dict[item.id] = {
            'item': item,
            'children': [],
            'is_active': current_path == item.get_url(),
            'is_active_parent': False
        }
    
    for item_id in items_dict:
        item_data = items_dict[item_id]
        if item_data['item'].parent_id is None:
            menu_tree.append(item_data)
        else:
            parent_id = item_data['item'].parent_id
            if parent_id in items_dict:
                items_dict[parent_id]['children'].append(item_data)
                if item_data['is_active']:
                    items_dict[parent_id]['is_active_parent'] = True

    return {'menu_tree': menu_tree}