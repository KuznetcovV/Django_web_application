from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson, CancelledLesson, TransferredLesson, Student
from .forms import LessonForm, LessonForStudentForm
from datetime import date, timedelta, datetime, time
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
def create_lesson_for_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = LessonForStudentForm(request.POST)
    else:
        form = LessonForStudentForm()

    if request.method == 'POST' and form.is_valid():
        form.instance.student = student
        form.save()
        return redirect('student_info', student_id=student_id)
    
    context = {
        'form': form,
        'student': student
    }

    return render(request, 'lessons/add_lesson_for_student.html', context)

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

        slots = calculate_free_intervals(d)
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
                day_lessons.append({
                    'lesson': lesson,
                    'time_start': lesson.time_start,
                    'time_end': lesson.time_end,
                    'is_transfered': False
                })
                added_lessons_ids.add(lesson.id)


        transferred_to = TransferredLesson.objects.filter(new_date=d)

        for row in transferred_to:
            if row.lesson.id not in added_lessons_ids:
                day_lessons.append({'lesson': row.lesson,
                                    'time_start': row.new_time_start or row.lesson.time_start,
                                    'time_end': row.new_time_end or row.lesson.time_end,
                                    'is_transfered': True})
                added_lessons_ids.add(row.lesson.id)

        schedule.append({
            'weekday': WEEKDAYS[d.weekday()],
            'date': d,
            'lessons': day_lessons,
            'slots': slots
        })


    context = {'schedule': schedule, 'today': today}
    return render(request, 'lessons/actual_schedule.html', context)

def is_conflict(start, end, busy):
    for b_start, b_end in busy:
        if start < b_end and end > b_start:
            return True
    return False

def calculate_free_intervals(date):
    weekday = date.weekday() + 1
    base_lessons = Lesson.objects.filter(day=weekday)
    transfer_to_lessons = TransferredLesson.objects.filter(new_date=date)
    busy = []
    for l in base_lessons:
        is_transfered_from = TransferredLesson.objects.filter(lesson=l, old_date=date).exists()
        is_canceled = CancelledLesson.objects.filter(lesson=l, date=date).exists()

        if not is_transfered_from and not is_canceled:
            busy.append((l.time_start, l.time_end))
    
    for t in transfer_to_lessons:
        if t.new_time_start and t.new_time_end:
            busy.append((t.new_time_start, t.new_time_end))
        else:
            busy.append((t.lesson.time_start, t.lesson.time_end))
    
    
    intervals_for_this_day = []
    current = time(10, 0)
    end_day = time(22, 0)

    while current < end_day:
        start_dt = datetime.combine(date, current)
        end_dt = start_dt + timedelta(hours=1)

        start = start_dt.time()
        end = end_dt.time()

        busy_flag = is_conflict(start, end, busy)

        intervals_for_this_day.append({'start_time': start,
                                       'end_time': end,
                                       'busy': busy_flag})
        
        current = end
    
    return intervals_for_this_day

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
    new_time_str = request.POST.get('new_time')

    if not (lesson_id and old_date_str and new_date_str and new_time_str):
        return redirect('actual_schedule')
    
    old_date = datetime.strptime(old_date_str, "%Y-%m-%d").date()
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
    new_time = datetime.strptime(new_time_str, '%H:%M').time()

    new_start = new_time
    new_end = (datetime.combine(date.today(), new_time) + timedelta(hours=1)).time()

    existing_transfer = TransferredLesson.objects.filter(lesson_id=lesson_id).first()

    if existing_transfer:
        existing_transfer.new_date = new_date
        existing_transfer.new_time_start = new_start
        existing_transfer.new_time_end = new_end
        existing_transfer.save()
    else:
        TransferredLesson.objects.create(
            lesson_id=lesson_id,
            old_date=old_date,
            new_date=new_date,
            new_time_start=new_start,
            new_time_end=new_end
        )

    return redirect('actual_schedule')
