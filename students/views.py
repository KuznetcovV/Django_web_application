from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm


# Create your views here.
def students_tab(request):
    students = Student.objects.order_by('name')
    return render(request, 'students/students.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')

    form = StudentForm()
    CLASS_CHOICES = [i for _, i in Student.CLASS_CHOICES]
    context = {
        'form': form,
        'classes': CLASS_CHOICES
    }

    return render(request, 'students/add_student.html', context)