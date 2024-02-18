from django.shortcuts import render


def menu_item(request, menu_item_title):
    return render(request, 'index.html')
