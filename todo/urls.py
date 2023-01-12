from django.urls import path
from .views import *

app_name = 'todo'
urlpatterns = [
    path('', list_view, name='list'),
    path('create/', create_view, name='create'),
    path('delete<slug>/', delete_view, name='delete'),
    path('update<slug>/', update_view, name='update'),
]
