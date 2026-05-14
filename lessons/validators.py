from django.core.exceptions import ValidationError
from .models import Lesson

def validate_lesson_overlap(weekday,
                            time_start,
                            time_end,
                            lesson_id=None):

    lessons_for_weekday = Lesson.objects.filter(day=weekday)

    if lesson_id:
        lessons_for_weekday = lessons_for_weekday.exclude(id=lesson_id)
    
    for lesson in lessons_for_weekday:
        if time_start < lesson.time_end and time_end > lesson.time_start:
            raise ValidationError('Указанное время пересекается с существующим занятием!')


def validate_start_less_end(time_start, time_end):
    if time_start >= time_end:
        raise ValidationError('Время начала занятия не может быть больше или равно времени конца занятия.')