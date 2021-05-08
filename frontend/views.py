# Copyright 2021 Radio Moreeni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from radioepg.models import Service, Bearer


def index(request):
    """Renders the index page."""
    return render(request, 'frontend/index.html')


@login_required
def service(request):
    """Renders the Service Information page when authenticated."""
    return render(request, 'frontend/service.html')


@login_required
def slideshow(request):
    """Renders the Visual Slideshow page when authenticated."""
    bearer = Bearer.objects.filter(service=Service.objects.first(), platform='ip').first()
    try:
        destination = f'/topic/id/{bearer.service.fqdn}/{bearer.service.serviceIdentifier}'
    except AttributeError:
        try:
            bearer = Bearer.objects.filter(service=Service.objects.first(), platform='fm').first()
            integer, decimal = str(bearer.frequency).split('.')
            frequency = f'{integer.rjust(3, "0")}{decimal.ljust(2, "0")}'
            destination = f'/topic/fm/{bearer.pi:1}{bearer.ecc}/{bearer.pi}/{frequency}'
        except AttributeError:
            destination = None
    context = {'bearer': destination}
    return render(request, 'frontend/slideshow.html', context)


@login_required
def gallery(request):
    """Renders the Visual Slideshow page when authenticated."""
    return render(request, 'frontend/gallery.html')


@login_required
def account(request):
    """Renders the account detail page."""
    return render(request, 'frontend/account.html')
