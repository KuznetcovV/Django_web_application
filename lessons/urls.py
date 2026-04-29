from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons_tab, name='lessons'),
    path('add-lesson/', views.add_lesson, name='add_lesson'),
    path('<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('base_schedule/', views.base_schedule_tab, name='base_schedule'),
    path('actual_shedule/', views.actual_schedule_view, name='actual_schedule'),
    path('cancel/', views.cancel_lesson, name='cancel_lesson'),
    path('transfer/', views.transfer_lesson, name='transfer_lesson')
]