from django.shortcuts import render, redirect
from .models import Lesson
from .forms import LessonForm


def schedule_tab(request):
    lessons = Lesson.objects.order_by('student')
    context = {
        'lessons': lessons
    }
    return render(request, 'schedule/schedule.html', context)


def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
    else:
        form = LessonForm()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule')

    context = {
        'form': form,
    }

    return render(request, 'schedule/add_lesson.html', context)
