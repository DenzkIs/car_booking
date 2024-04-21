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
    start = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    finish = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
