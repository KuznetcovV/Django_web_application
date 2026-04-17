from .models import Student
from django.forms import ModelForm, Select, TextInput


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'number_of_class']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя ученика'
                }),
            'number_of_class': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите класс ученика'
                }),
        }