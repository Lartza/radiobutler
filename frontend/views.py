import subprocess
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from radioepg.models import Service, Bearer


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
    destination = None
    try:
        bearer = Bearer.objects.filter(service=Service.objects.first(), platform='ip').first()
        destination = f'/topic/id/{bearer.service.fqdn}/{bearer.service.serviceIdentifier}'
    except Bearer.DoesNotExist:
        try:
            bearer = Bearer.objects.filter(service=Service.objects.first(), platform='fm').first()
            integer, decimal = str(bearer.frequency).split('.')
            frequency = f'{integer.rjust(3, "0")}{decimal.ljust(2, "0")}'
            destination = f'/topic/fm/{bearer.pi:1}{bearer.ecc}/{bearer.pi}/{frequency}'
        except Bearer.DoesNotExist:
            pass
    context = {'commit': get_commit(),
               'bearer': destination}
    return render(request, 'frontend/slideshow.html', context)


@login_required
def gallery(request):
    """Renders the Visual Slideshow page when authenticated."""
    context = {'commit': get_commit()}
    return render(request, 'frontend/gallery.html', context)
