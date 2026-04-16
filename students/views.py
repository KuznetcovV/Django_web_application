from django.shortcuts import render

# Create your views here.
def students_tab(request):
    return render(request, 'students/students.html')