from django import forms
from datetime import datetime
from rental.models import MotorcycleReservation


class MotorcycleReservationForm(forms.ModelForm):
    template_name = 'bike_detail.html'

    class Meta:
        model = MotorcycleReservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control start-date', 'id': 'from'}),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control end-date', 'id': 'to'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        try:
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            current_date = datetime.now().date()

            if start_date >= current_date and end_date >= current_date and not end_date < start_date:
                return cleaned_data
            else:
                self.add_error(None, 'Invalid date format.')
        except TypeError:
            self.add_error(None, 'Invalid date format.')
