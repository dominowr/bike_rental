from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from django.core.mail import send_mail
from contact.forms import ContactForm


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return redirect('contact:contact')

    def form_valid(self, form):

        data = form.cleaned_data

        send_mail(
            subject=data['subject'],
            message=f"Email from address: {data['email']}.\n\n{data['message']}",
            from_email=settings.EMAIL,
            recipient_list=[settings.EMAIL],
            fail_silently=False,
        )

        messages.success(self.request, 'Your email was send successfully.')

        return redirect('contact:contact')
