from django.db import models


class Student(models.Model):

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    CLASS_CHOICES = [(i, f'{i}-й класс') for i in range(1, 12)]

    name = models.CharField(verbose_name='Имя ученика', max_length=100)
    number_of_class = models.IntegerField(verbose_name='Класс ученика', choices=CLASS_CHOICES)

    def __str__(self):
        return f'{self.name} {self.number_of_class}'
    

class Subscription(models.Model):

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')

    start_date = models.DateField()
    end_date = models.DateField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
