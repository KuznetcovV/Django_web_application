from django.shortcuts import render


def home_tab(request):
    return render(request, 'home/home_tab.html')
