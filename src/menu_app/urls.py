from django.urls import path

from .views import menu_item


urlpatterns = [
    path('<str:menu_item_title>/', menu_item, name='menu_item'),
]
