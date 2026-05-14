from django.core.exceptions import ValidationError
import re
from .models import Student

def validate_student_name(name):
    pattern = r'^[А-Яа-яA-Za-z-]+\s[А-Яа-яA-Za-z-]+$'
    check = re.fullmatch(pattern, name)
    if not check:
        raise ValidationError('Некорректное имя')
    
    if Student.objects.filter(name=name).exists():
        raise ValidationError('Ученик с таким именем уже есть.')


def validate_subscription_price(price):
    if price <= 0:
        raise ValidationError('Цена занятия не может быть меньше или равна 0')
    

def validate_lesson_overlap(
    start_date_check,
    end_date_check
):
    if start_date_check and end_date_check and start_date_check >= end_date_check:
        ValidationError('Дата начала не может быть больше или равна дате конца абонемента')