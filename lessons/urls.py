from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons_tab, name='lessons'),
    path('add-lesson', views.add_lesson, name='add_lesson'),
    path('<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson')
]