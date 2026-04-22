from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson
from .forms import LessonForm


@login_required
def lessons_tab(request):
    lessons = Lesson.objects.order_by('student')
    context = {
        'lessons': lessons
    }
    return render(request, 'lessons/lessons.html', context)


@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
    else:
        form = LessonForm()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lessons')

    context = {
        'form': form,
    }

    return render(request, 'lessons/add_lesson.html', context)


@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lessons')
    else:
        form = LessonForm(instance=lesson)

    context = {'form': form}

    return render(request, 'lessons/edit_lesson.html', context)


@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        lesson.delete()

    return redirect('lessons')
