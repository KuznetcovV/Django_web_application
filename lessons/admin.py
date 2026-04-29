from django.contrib import admin
from .models import Lesson, CancelledLesson, TransferredLesson


admin.site.register(Lesson)
admin.site.register(CancelledLesson)
admin.site.register(TransferredLesson)
