from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'frontend/index.html')


@login_required
def service(request):
    return render(request, 'frontend/service.html')
