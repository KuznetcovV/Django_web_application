from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_tab, name='students'),
    path('add-student', views.add_student, name='add_student'),
    path('<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('<int:student_id>/info/', views.student_info, name='student_info'),
    path('<int:student_id>/subscription/create/', views.create_subscription, name='create_subscription'),
    path('<int:student_id>/lessons/', views.student_lessons ,name='student_lessons'),
    path('<int:student_id>/logs/', views.student_logs , name='student_logs'),
    path('<int:student_id>/subscriptions/', views.student_subscriptions , name='student_subscriptions')
]