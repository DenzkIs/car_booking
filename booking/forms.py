from django import forms
from .models import CarNote


class CarNoteForm(forms.ModelForm):

    class Meta:
        model = CarNote
        fields = ('city', 'taking_time', 'return_time', 'comment')

