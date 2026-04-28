from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson, CancelledLesson
from .forms import LessonForm
from datetime import date, timedelta, datetime
from django.views.decorators.http import require_POST


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


@login_required
def base_schedule_tab(request):
    schedule = {i: [] for i in range(1, 8)}

    lessons = Lesson.objects.all()

    for lesson in lessons:
        schedule[lesson.day].append(lesson)

    context = {'schedule': schedule}

    return render(request, 'lessons/base_schedule.html', context)


def actual_schedule_view(request):
    today = date.today()
    start_week = today - timedelta(days=today.weekday())

    week_dates = [start_week + timedelta(days=i) for i in range(7)]

    schedule = []

    for d in week_dates:
        weekday = d.weekday() + 1

        lessons = Lesson.objects.filter(day=weekday)

        day_lessons = []

        for lesson in lessons:
            is_cancelled = CancelledLesson.objects.filter(
                lesson=lesson,
                date=d
            ).exists()

            if not is_cancelled:
                day_lessons.append(lesson)

        schedule.append({
            'date': d,
            'lessons': day_lessons
        })

    return render(request, 'lessons/actual_schedule.html', {'schedule': schedule})


@require_POST
def cancel_lesson(request):
    lesson_id = request.POST.get('lesson_id')
    date_str = request.POST.get('date')

    lesson_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    CancelledLesson.objects.get_or_create(
        lesson_id=lesson_id,
        date=lesson_date
    )

    return redirect('actual_schedule')
