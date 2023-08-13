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
