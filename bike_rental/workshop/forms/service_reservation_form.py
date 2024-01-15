from django import forms
from django.utils import timezone
from datetime import datetime, time
from workshop.models import ServiceReservation


class ServiceReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'datepicker'})
    )
    hour = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'timepicker'})
    )

    class Meta:
        model = ServiceReservation
        fields = ['date', 'hour']

    def clean(self):
        cleaned_data = super().clean()
        current_date = datetime.now().date()
        open_hour = time(7, 0)
        close_hour = time(16, 0)

        try:
            selected_date = cleaned_data.get('date')
            selected_hour = datetime.strptime(cleaned_data.get('hour'), '%I:%M %p').time()
            if selected_date >= current_date and open_hour <= selected_hour <= close_hour:
                date_time = timezone.make_aware(datetime.combine(
                    selected_date, selected_hour
                ))
                cleaned_data['date_time'] = date_time
                return cleaned_data
            else:
                self.add_error(None, 'Sorry, we are closed.')
        except ValueError:
            self.add_error(None, 'Invalid date or time format.')
