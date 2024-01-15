from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(), max_length=500)
    email = forms.EmailField()

    def clean_message(self):
        message = self.cleaned_data.get('message')

        if len(message) < 20:
            self.add_error(None, 'Message should be at least 20 characters long.')

        return message

