from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def stockTracker(request):
    return render(request, 'stockTracker.html')
