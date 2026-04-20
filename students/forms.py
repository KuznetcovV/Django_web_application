from .models import Student
from django.forms import ModelForm, Select, TextInput, ChoiceField


class StudentForm(ModelForm):
    number_of_class = ChoiceField(
        label='Класс ученика',
        choices=[('', 'Выберите класс')] + Student.CLASS_CHOICES
        )

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
                }),
        }
