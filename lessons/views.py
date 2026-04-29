from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson, CancelledLesson, TransferredLesson
from .forms import LessonForm
from datetime import date, timedelta, datetime
from django.views.decorators.http import require_POST


WEEKDAYS = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье',
}

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
        added_lessons_ids = set()

        for lesson in lessons:
            is_cancelled = CancelledLesson.objects.filter(
                lesson=lesson,
                date=d
            ).exists()

            is_transferred_from = TransferredLesson.objects.filter(
                lesson=lesson,
                old_date=d,
            ).exists()

            if not is_cancelled and not is_transferred_from:
                day_lessons.append(lesson)
                added_lessons_ids.add(lesson.id)


        transferred_to = TransferredLesson.objects.filter(new_date=d)

        for row in transferred_to:
            if row.lesson.id not in added_lessons_ids:
                day_lessons.append(row.lesson)
                added_lessons_ids.add(row.lesson.id)

        schedule.append({
            'weekday': WEEKDAYS[d.weekday()],
            'date': d,
            'lessons': day_lessons,
        })


        context = {'schedule': schedule, 'today': today}
    return render(request, 'lessons/actual_schedule.html', context)


@require_POST
def cancel_lesson(request):
    lesson_id = request.POST.get('lesson_id')
    date_str = request.POST.get('date')

    lesson_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    transfer_for_cancel = TransferredLesson.objects.filter(
        lesson_id=lesson_id,
        new_date=lesson_date
    )

    if transfer_for_cancel.exists():
        transfer_for_cancel.delete()
        

    CancelledLesson.objects.update_or_create(
        lesson_id=lesson_id,
        date=lesson_date
    )

    return redirect('actual_schedule')


@require_POST
def transfer_lesson(request):
    lesson_id = request.POST.get('lesson_id')
    old_date_str = request.POST.get('old_date')
    new_date_str = request.POST.get('new_date')

    if not (lesson_id and old_date_str and new_date_str):
        return redirect('actual_schedule')
    
    old_date = datetime.strptime(old_date_str, "%Y-%m-%d").date()
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()

    existing_transfer = TransferredLesson.objects.filter(
        lesson_id=lesson_id
    ).first()

    if existing_transfer:
        existing_transfer.new_date = new_date
        existing_transfer.save()
    else:
        TransferredLesson.objects.update_or_create(
            lesson_id=lesson_id,
            old_date=old_date,
            defaults={
                'new_date': new_date
            }
        )

    return redirect('actual_schedule')
