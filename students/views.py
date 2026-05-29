from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Subscription
from lessons.models import Lesson
from .forms import StudentForm, SubscriptionForm
from datetime import timedelta


@login_required
def students_tab(request):
    students = Student.objects.order_by('name')
    context = {
        'students': students
    }
    return render(request, 'students/students.html', context)


def create_subscription(requset, student_id):

    student = get_object_or_404(Student, id=student_id)
    if requset.method == 'POST':
        form = SubscriptionForm(requset.POST)
    else:
        form = SubscriptionForm()
    
    
    if requset.method == 'POST' and form.is_valid():
        form.instance.student = student
        form.save()
        return redirect('student_info', student_id=student_id)
    
    context = {
        'form': form,
        'student': student
    }

    return render(requset, 'students/create_subscription.html', context)


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
    else:
        form = StudentForm()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('students')

    context = {
        'form': form,
    }

    return render(request, 'students/add_student.html', context)


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    context = {'form': form}

    return render(request, 'students/edit_student.html', context)


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()

    return redirect('students')



@login_required
def student_info(request, student_id):

    student = get_object_or_404(
        Student.objects.prefetch_related(
            'lessons',
            'subscriptions',
            'lesson_logs'
        ),
        id=student_id
    )

    lessons = student.lessons.all()

    subscriptions = student.subscriptions.all()

    lesson_logs = student.lesson_logs.order_by('-date')

    context = {
        'student': student,
        'lessons': lessons,
        'subscriptions': subscriptions,
        'lesson_logs': lesson_logs
    }

    return render(request, 'students/student_info.html', context)


def count_lessons_for_student_in_period(start_date, end_date, student_id):
    current = start_date
    end = end_date
    counter_of_lessons_in_period = 0
    lessons_weekdays = set()
    for lesson in Lesson.objects.filter(student_id=student_id):
        lessons_weekdays.add(lesson.day)
    while current <= end:
        if current.weekday() + 1 in lessons_weekdays:
            counter_of_lessons_in_period += 1
        current += timedelta(days=1)
    return counter_of_lessons_in_period


def count_price_sibscription(student_id):
    subsctiption_for_student = Subscription.objects.filter(student=student_id).order_by('-start_date').first()
    start_date = subsctiption_for_student.start_date
    end_date = subsctiption_for_student.end_date
    price_for_one_lesson = subsctiption_for_student.price
    amount_of_lessons = count_lessons_for_student_in_period(start_date, end_date, student_id)
    return int(price_for_one_lesson * amount_of_lessons)


def student_logs(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    lesson_logs = student.lesson_logs.order_by('-date')

    context = {
        'student': student,
        'lesson_logs': lesson_logs
    }

    return render(request, 'students/student_logs.html', context)


def student_lessons(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    lessons = student.lessons.order_by('day')

    context = {
        'student': student,
        'lessons': lessons
    }

    return render(request, 'students/student_lessons.html', context)


def student_subscriptions(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    subscriptions = student.subscriptions.order_by('-end_date')

    context = {
        'student': student,
        'subscriptions': subscriptions
    }

    return render(request, 'students/student_subscriptions.html', context)