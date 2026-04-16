from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home_tab),
    path('students/', include('students.urls')),
    path('schedule/', include('schedule.urls'))
]