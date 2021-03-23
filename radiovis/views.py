import time
import stomp

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from stomp.exception import ConnectFailedException

from radiodns.settings import STOMP_HOST, STOMP_PORT, STOMP_USERNAME, STOMP_PASSWORD

from .models import ImageSlide
from .serializers import ImageSlideSerializer


class ErrorListener(stomp.ConnectionListener):
    def __init__(self):
        self.error = None

    def on_error(self, headers, body):
        self.error = body


class ImageSlideViewSet(viewsets.ModelViewSet):
    queryset = ImageSlide.objects.all()
    serializer_class = ImageSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def send(self, request, pk=None):  # pylint: disable=unused-argument
        headers = {}
        slide = self.get_object()

        if slide.trigger_time:
            headers['trigger_time'] = slide.trigger_time.isoformat()
        else:
            headers['trigger_time'] = 'NOW'

        if slide.link:
            headers['link'] = slide.link

        try:
            # Reduce blocking by reconnecting only once
            conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
            # Create listener to catch errors from Stomp
            lst = ErrorListener()
            conn.set_listener('', lst)
            conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
            conn.send(body=f'SHOW {request.scheme}://{request.META.get("HTTP_HOST")}{slide.image.url}',
                      headers=headers,
                      destination='/topic/fm/6e1/6024/09840/image')
            conn.disconnect()
            time.sleep(2)

            if lst.error:
                return Response(f'{lst.error}', status=status.HTTP_502_BAD_GATEWAY)
            slide.sent = True
            slide.save()

            return Response(f'Sent: SHOW {request.scheme}://{request.META.get("HTTP_HOST")}{slide.image.url}'
                            f' headers: {headers}')
        except ConnectFailedException:
            return Response(f'Connection to stomp server {STOMP_HOST}:{STOMP_PORT} failed',
                            status=status.HTTP_502_BAD_GATEWAY)


class TextSlideViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):  # pylint: disable=unused-argument,no-self-use
        text = request.data['text']

        try:
            conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
            lst = ErrorListener()
            conn.set_listener('', lst)
            conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
            conn.send(body=f'TEXT {text}',
                      destination='/topic/fm/6e1/6024/09840/text')
            conn.disconnect()
            time.sleep(2)
            if lst.error:
                return Response(f'{lst.error}', status=status.HTTP_502_BAD_GATEWAY)
            return Response(f'Sent: TEXT {text}')
        except ConnectFailedException:
            return Response(f'Connection to stomp server {STOMP_HOST}:{STOMP_PORT} failed',
                            status=status.HTTP_502_BAD_GATEWAY)
