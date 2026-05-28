from .models import Lesson, LessonLog
from django.forms import ModelForm
from django import forms
from .validators import validate_lesson_overlap, validate_start_less_end


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

    def clean(self):

        cleaned_data = super().clean()
        weekday = cleaned_data.get('day')
        time_start = cleaned_data.get('time_start')
        time_end = cleaned_data.get('time_end')

        if not (weekday and time_start and time_end):
            return cleaned_data
        validate_start_less_end(time_start, time_end)
        validate_lesson_overlap(weekday,
                                time_start,
                                time_end,
                                self.instance.id)
        return cleaned_data


class LessonForStudentForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ['student']
        widgets = {
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
    
    def clean(self):
        cleaned_data = super().clean()
        weekday = cleaned_data.get('day')
        time_start = cleaned_data.get('time_start')
        time_end = cleaned_data.get('time_end')
        validate_lesson_overlap(weekday,
                                time_start,
                                time_end)
        return cleaned_data
    

class LessonLogForm(ModelForm):
    class Meta:
        model = LessonLog
        exclude = ['student', 'lesson', 'date']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема занятия'
            }),
            'textbook': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Учебник'
            }),
            'solved_tasks': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Решеные задания',
                'rows': 3
            }),
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Оценка',
                'min': 1,
                'max': 5
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий о занятии'
            })
        }