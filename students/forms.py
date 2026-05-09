from .models import Student, Subscription
from django.forms import ModelForm
from django import forms


class StudentForm(ModelForm):
    number_of_class = forms.ChoiceField(
        label='Класс ученика',
        choices=[('', 'Выберите класс')] + Student.CLASS_CHOICES
        )

    class Meta:
        model = Student
        fields = ['name', 'number_of_class']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя ученика'
                }),
            'number_of_class': forms.Select(attrs={
                'class': 'form-control',
                }),
        }


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ['student']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
                }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
                }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена одного занятия'}),

            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                }),
        }