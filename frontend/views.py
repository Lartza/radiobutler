import subprocess
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def get_commit():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode()


def index(request):
    context = {'commit': get_commit()}
    return render(request, 'frontend/index.html', context)


@login_required
def service(request):
    context = {'commit': get_commit()}
    return render(request, 'frontend/service.html', context)


@login_required
def slideshow(request):
    context = {'commit': get_commit()}
    return render(request, 'frontend/slideshow.html', context)
