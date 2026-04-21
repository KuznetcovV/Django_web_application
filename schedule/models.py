from django.db import models
from students.models import Student


class Lesson(models.Model):

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]

    student = models.ForeignKey(Student, verbose_name='Ученик', on_delete=models.CASCADE)
    day = models.IntegerField(verbose_name='День недели', choices=DAYS_OF_WEEK)
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время конца занятия')

    def __str__(self):
        return f'{self.student} - {self.get_day_display()}: {self.time_start}-{self.time_end}'