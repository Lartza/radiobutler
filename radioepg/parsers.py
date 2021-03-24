import json

from django.conf import settings
from django.http.multipartparser import MultiPartParserError
from django.http.multipartparser import \
    MultiPartParser as DjangoMultiPartParser
from rest_framework.exceptions import ParseError

from rest_framework.parsers import BaseParser, DataAndFiles


class ServiceInformationParser(BaseParser):

    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = request.upload_handlers

        try:
            parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
            data, files = parser.parse()
            return DataAndFiles(data, files)
        except MultiPartParserError as exc:
            raise ParseError('Multipart form parse error - %s' % str(exc))
