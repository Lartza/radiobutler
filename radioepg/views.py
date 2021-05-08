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

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from drf_nested_forms.parsers import NestedMultiPartParser

from .models import Service, Bearer
from .serializers import ServiceSerializer, BearerSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, NestedMultiPartParser]


class BearerViewSet(viewsets.ModelViewSet):
    queryset = Bearer.objects.all()
    serializer_class = BearerSerializer
    permission_classes = [permissions.IsAuthenticated]


def service_information(request):
    """Renders a dynamic SI.xml file.

    If a logo exists, add resized versions of it to context.

    If bearers exist, form XML elements of them in the proper platform format to context.
    """
    services = Service.objects.all()
    for service in services:
        bearer_elements = []
        for bearer in service.bearers.all():
            if bearer.platform == 'fm':
                # Frequency needs to be formatted with five integers, zero padded on both sides
                integer, decimal = str(bearer.frequency).split('.')
                frequency = f'{integer.rjust(3, "0")}{decimal.ljust(2, "0")}'
                bearer_element = f'<bearer id="fm:{bearer.pi[0]}{bearer.ecc}.{bearer.pi}.{frequency}" ' \
                                 f'cost="{bearer.cost}"/>'
            elif bearer.platform == 'ip':
                bearer_element = f'<bearer id="{bearer.url}" mimeValue="{bearer.mimeValue}" cost="{bearer.cost}"'
                if bearer.bitrate:
                    bearer_element += f' bitrate="{bearer.bitrate}"'
                bearer_element += '/>'
            bearer_elements.append(bearer_element)
        service.bearer_elements = bearer_elements

    context = {'services': services}

    return render(request, 'radioepg/SI.xml', context, content_type='text/xml')
