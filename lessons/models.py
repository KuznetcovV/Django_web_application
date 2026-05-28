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


class CancelledLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('lesson', 'date')

    def __str__(self):
        return f'{self.lesson} - {self.date}'


class TransferredLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    old_date = models.DateField()
    new_date = models.DateField()

    new_time_start = models.TimeField(null=True, blank=True)
    new_time_end = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'old_date')
    
    def __str__(self):
        return f'{self.lesson}: {self.old_date} - {self.new_date}'
    

class LessonLog(models.Model):
    student = models.ForeignKey(Student, 
                                on_delete=models.CASCADE,
                                related_name='lesson_logs')
    
    lesson = models.ForeignKey(Lesson, 
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    
    date = models.DateField()
    topic = models.CharField(
        max_length=255,
        blank=True
    )

    textbook = models.CharField(
        max_length=255,
        blank=True
    )

    solved_tasks = models.TextField(
        blank=True
    )

    grade = models.IntegerField(
        blank=True,
        null=True
    )

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student} {self.date}'