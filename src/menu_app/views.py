from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def menu_item(request, menu_item_title):
    menu_item = get_object_or_404(MenuItem, title=menu_item_title)
    return render(request, 'index.html', {'menu_item': menu_item})
