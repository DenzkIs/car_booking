import datetime

from django import forms
from .models import CarNote, CarServiceInfo


class CarNoteForm(forms.ModelForm):

    class Meta:
        model = CarNote
        fields = ('city', 'taking_time', 'return_time', 'comment')


class CarServiceInfoForm(forms.ModelForm):

    class Meta:
        model = CarServiceInfo
        fields = '__all__'


class ChooseTimeRange(forms.Form):
    day_today = datetime.date.today()
    start = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'value': "2024-01-01"}), label='От')
    finish = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'value': day_today}), label='До')
