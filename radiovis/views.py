import time
from datetime import datetime, timezone

import stomp

from django.db.models import ProtectedError

from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from stomp.exception import ConnectFailedException

from radiodns.settings import STOMP_HOST, STOMP_PORT, STOMP_USERNAME, STOMP_PASSWORD

from .models import ImageSlide, TextSlide, Image
from .serializers import ImageSlideSerializer, TextSlideSerializer, ImageSerializer


def send_stomp_image(instance, url):
    headers = {}

    if instance.trigger_time:
        headers['trigger_time'] = instance.trigger_time.isoformat()
    else:
        headers['trigger_time'] = 'NOW'

    if instance.link:
        headers['link'] = instance.link

    try:
        # Reduce blocking by reconnecting only once
        conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
        # Create listener to catch error messages from Stomp
        lst = ErrorListener()
        conn.set_listener('', lst)

        conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
        conn.send(body=f'SHOW {url}',
                  headers=headers,
                  destination='/topic/fm/6e1/6024/09840/image')
        conn.disconnect()
        time.sleep(2)

        # Check for received error messages
        if lst.error:
            raise stomp.exception.StompException(f'{lst.error}')
        instance.sent = datetime.now(timezone.utc)
        instance.save()
    except (ConnectFailedException, stomp.exception.StompException):
        raise


def send_stomp_text(instance):
    try:
        # Reduce blocking by reconnecting only once
        conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
        # Create listener to catch error messages from Stomp
        lst = ErrorListener()
        conn.set_listener('', lst)

        conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
        conn.send(body=f'TEXT {instance.message}',
                  destination='/topic/fm/6e1/6024/09840/text')
        conn.disconnect()
        time.sleep(2)

        # Check for received error messages
        if lst.error:
            raise stomp.exception.StompException(f'{lst.error}')
        instance.sent = datetime.now(timezone.utc)
        instance.save()
    except ConnectFailedException:
        raise


class ErrorListener(stomp.ConnectionListener):
    """Listener for making error messages from the server available."""
    def __init__(self):
        """Initializes instance variables."""
        self.error = None

    def on_error(self, headers, body):
        """Stores received error."""
        self.error = body


class ImageSlideViewSet(viewsets.ModelViewSet):
    queryset = ImageSlide.objects.all()
    serializer_class = ImageSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_stomp_image(instance, self.request.build_absolute_uri(instance.image.image.url))

    def destroy(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            e = str(e).split(',', 1)
            return Response({'error': e[0].strip("('"), 'object': e[1].strip(" )")}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response('Image is linked to a slide that has to be stored for 21 days due to legal requirements',
                            status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
