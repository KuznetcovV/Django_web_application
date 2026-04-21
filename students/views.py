from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def students_tab(request):
    students = Student.objects.order_by('name')
    context = {
        'students': students
    }
    return render(request, 'students/students.html', context)


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


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()

    return redirect('students')