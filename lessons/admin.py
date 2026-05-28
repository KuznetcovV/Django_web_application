from django.contrib import admin
from .models import Lesson, CancelledLesson, TransferredLesson, LessonLog


admin.site.register(Lesson)
admin.site.register(CancelledLesson)
admin.site.register(TransferredLesson)
admin.site.register(LessonLog)
