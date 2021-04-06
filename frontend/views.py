import subprocess
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def get_commit():
    """Returns short commit hash of HEAD."""
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode()


def index(request):
    """Renders the index page."""
    context = {'commit': get_commit()}
    return render(request, 'frontend/index.html', context)


@login_required
def service(request):
    """Renders the Service Information page when authenticated."""
    context = {'commit': get_commit()}
    return render(request, 'frontend/service.html', context)


@login_required
def slideshow(request):
    """Renders the Visual Slideshow page when authenticated."""
    context = {'commit': get_commit()}
    return render(request, 'frontend/slideshow.html', context)


@login_required
def gallery(request):
    """Renders the Visual Slideshow page when authenticated."""
    context = {'commit': get_commit()}
    return render(request, 'frontend/gallery.html', context)
