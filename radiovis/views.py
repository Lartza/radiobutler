import time
import stomp

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from stomp.exception import ConnectFailedException

from radiodns.settings import STOMP_HOST, STOMP_PORT, STOMP_USERNAME, STOMP_PASSWORD

from .models import ImageSlide, TextSlide
from .serializers import ImageSlideSerializer, TextSlideSerializer


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

    def create(self, request, *args, **kwargs):
        """Sends SHOW messages to Stomp server."""
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
            # Create listener to catch error messages from Stomp
            lst = ErrorListener()
            conn.set_listener('', lst)

            conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
            conn.send(body=f'SHOW {request.scheme}://{request.META.get("HTTP_HOST")}{slide.image.url}',
                      headers=headers,
                      destination='/topic/fm/6e1/6024/09840/image')
            conn.disconnect()
            time.sleep(2)

            # Check for received error messages
            if lst.error:
                return Response(f'{lst.error}', status=status.HTTP_502_BAD_GATEWAY)
            slide.sent = True
            slide.save()

            return super().create(request, *args, **kwargs)
        except ConnectFailedException:
            return Response(f'Connection to stomp server {STOMP_HOST}:{STOMP_PORT} failed',
                            status=status.HTTP_502_BAD_GATEWAY)


class TextSlideViewSet(viewsets.ModelViewSet):
    queryset = TextSlide.objects.all()
    serializer_class = TextSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Send TEXT messages to Stomp server without creating any objects."""
        text = request.data['text']

        try:
            # Reduce blocking by reconnecting only once
            conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)], reconnect_attempts_max=1)
            # Create listener to catch error messages from Stomp
            lst = ErrorListener()
            conn.set_listener('', lst)

            conn.connect(STOMP_USERNAME, STOMP_PASSWORD, wait=True)
            conn.send(body=f'TEXT {text}',
                      destination='/topic/fm/6e1/6024/09840/text')
            conn.disconnect()
            time.sleep(2)

            # Check for received error messages
            if lst.error:
                return Response(f'{lst.error}', status=status.HTTP_502_BAD_GATEWAY)
            return super().create(request, *args, **kwargs)
        except ConnectFailedException:
            return Response(f'Connection to stomp server {STOMP_HOST}:{STOMP_PORT} failed',
                            status=status.HTTP_502_BAD_GATEWAY)
