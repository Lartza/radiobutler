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

import time
from datetime import datetime, timezone

import stomp

from django.db.models import ProtectedError

from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from radiodns.settings import STOMP_HOST, STOMP_PORT, STOMP_USERNAME, STOMP_PASSWORD

from radioepg.models import Bearer
from .models import ImageSlide, TextSlide, Image
from .serializers import ImageSlideSerializer, TextSlideSerializer, ImageSerializer


def send_stomp_image(instance, url):
    headers = {}

    if instance.trigger_time:
        headers['trigger-time'] = str(instance.trigger_time.isoformat()).replace('+00:00', 'Z')
    else:
        headers['trigger-time'] = 'NOW'

    if instance.link:
        headers['link'] = instance.link

    # Reduce blocking by reconnecting only once
    conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
    # Create listener to catch error messages from Stomp
    lst = ErrorListener()
    conn.set_listener('', lst)

    conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
    bearers = Bearer.objects.all()
    if len(bearers) > 0:
        for bearer in bearers:
            if bearer.platform == 'fm':
                integer, decimal = str(bearer.frequency).split('.')
                frequency = f'{integer.rjust(3, "0")}{decimal.ljust(2, "0")}'
                destination = f'/topic/fm/{bearer.pi[0]}{bearer.ecc}/{bearer.pi}/{frequency}/image'
            elif bearer.platform == 'ip':
                destination = f'/topic/{bearer.service.serviceIdentifier}/image'
            conn.send(body=f'SHOW {url}',
                      headers=headers,
                      destination=destination)
        conn.disconnect()
        time.sleep(2)

        # Check for received error messages
        if lst.error:
            raise stomp.exception.StompException(f'{lst.error}')
        instance.sent = datetime.now(timezone.utc)
        instance.save()
    else:
        raise stomp.exception.StompException('No bearers configured')


def send_stomp_text(instance):
    # Reduce blocking by reconnecting only once
    conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
    # Create listener to catch error messages from Stomp
    lst = ErrorListener()
    conn.set_listener('', lst)

    conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
    bearers = Bearer.objects.all()
    if len(bearers) > 0:
        for bearer in bearers:
            if bearer.platform == 'fm':
                integer, decimal = str(bearer.frequency).split('.')
                frequency = f'{integer.rjust(3, "0")}{decimal.ljust(2, "0")}'
                destination = f'/topic/fm/{bearer.pi[0]}{bearer.ecc}/{bearer.pi}/{frequency}/text'
            elif bearer.platform == 'ip':
                destination = f'/topic/{bearer.service.serviceIdentifier}/text'
            conn.send(body=f'TEXT {instance.message}',
                      destination=destination)
        conn.disconnect()
        time.sleep(2)

        # Check for received error messages
        if lst.error:
            raise stomp.exception.StompException(f'{lst.error}')
        instance.sent = datetime.now(timezone.utc)
        instance.save()
    else:
        raise stomp.exception.StompException('No bearers configured')


class ErrorListener(stomp.ConnectionListener):
    """Listener for making error messages from the server available."""
    def __init__(self):
        """Initializes instance variables."""
        self.error = None

    def on_error(self, frame):
        """Stores received error."""
        self.error = frame.body


class ImageSlideViewSet(viewsets.ModelViewSet):
    queryset = ImageSlide.objects.all()
    serializer_class = ImageSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_stomp_image(instance, self.request.build_absolute_uri(instance.image.image.url))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except (stomp.exception.ConnectFailedException, stomp.exception.StompException) as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *_, **__):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            e = str(e).split(',', 1)
            return Response({'error': e[0].strip("('"), 'object': e[1].strip(" )")}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TextSlideViewSet(viewsets.ModelViewSet):
    queryset = TextSlide.objects.all()
    serializer_class = TextSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_stomp_text(instance)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except (stomp.exception.ConnectFailedException, stomp.exception.StompException) as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *_, **__):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            e = str(e).split(',', 1)
            return Response({'error': e[0].strip("('"), 'object': e[1].strip(" )")}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('-id')
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def destroy(self, request, *_, **__):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response('Image is linked to a slide that has to be stored for 21 days due to legal requirements',
                            status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
