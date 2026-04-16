from django.shortcuts import render


def schedule_tab(request):
    return render(request, 'schedule/schedule.html')