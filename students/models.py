from django.db import models


class Student(models.Model):

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    CLASS_CHOICES = [(i, f'{i}-й класс') for i in range(1, 12)]

    name = models.CharField(verbose_name='Имя ученика', max_length=100)
    number_of_class = models.IntegerField(verbose_name='Класс ученика', choices=CLASS_CHOICES)

    def __str__(self):
        # должна возвращать строку
        return f'{self.name} {self.number_of_class}'
