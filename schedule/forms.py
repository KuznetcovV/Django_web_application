from .models import Lesson
from django.forms import ModelForm
from django import forms


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите ученика'
                }),
            'day': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите день недели'}),
            'time_start': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'placeholder': 'Выберите время начала занятия'}),
            'time_end': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'placeholder': 'Выберите время конца занятия'}),
        }