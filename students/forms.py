from .models import Student, Subscription
from django.forms import ModelForm
from django import forms
from .validators import validate_student_name, validate_subscription_price, validate_subscription_dates



class StudentForm(ModelForm):
    number_of_class = forms.ChoiceField(
        label='Класс ученика',
        choices=[('', 'Выберите класс')] + Student.CLASS_CHOICES
        )    

    def clean_name(self):
        name = self.cleaned_data.get('name')

        validate_student_name(
            name,
            self.instance.id
        )

        return name

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
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        validate_subscription_price(price)
        return price


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        validate_subscription_dates(start_date, end_date)
        return cleaned_data