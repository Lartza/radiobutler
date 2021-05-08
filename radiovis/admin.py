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

from django.contrib import admin
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import ImageSlide, TextSlide


@admin.register(ImageSlide)
class ImageSlideAdmin(admin.ModelAdmin):
    readonly_fields = ['trigger_time', 'image', 'link', 'sent']

    def has_add_permission(self, request, obj=None):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except ProtectedError as e:
            self.message_user(request, str(e), messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(object_id,),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)


@admin.register(TextSlide)
class TextSlideAdmin(admin.ModelAdmin):
    readonly_fields = ['message', 'sent']

    def has_add_permission(self, request, obj=None):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except ProtectedError as e:
            self.message_user(request, str(e), messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(object_id,),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)
