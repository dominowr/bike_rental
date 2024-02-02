from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from workshop.models import Service


def get_unavailable_hours(slug):
    """
    Returns a dictionary of dates with unavailable hours for a specific service in str format.

    :param slug: service-slug.
    :return: Dictionary {date: [hour]}.
    """
    service = Service.objects.get(slug=slug)

    reservations = [
        timezone.template_localtime(r.date_time) for r in service.servicereservation_set.all()
    ]

    unavailable_hours = {}

    for r in reservations:
        date = r.date().strftime('%Y-%m-%d')
        hour = r.time().strftime('%I:%M %p')

        if date not in unavailable_hours:
            unavailable_hours[date] = [hour]
        else:
            unavailable_hours[date].append(hour)

    return unavailable_hours


def send_confirmation_mail(user, service, date, hour):
    """
    Sends a confirmation email with details of the workshop appointment to the user.

    :params user: The user making the appointment.
    :params service: The booked workshop service.
    :params date: The date of the appointment.
    :params hour: The scheduled hour of the appointment.
    """
    send_mail(
        subject='Workshop appointment confirmation',
        message=f'''
        Dear {user.first_name},
        
        We are delighted to confirm your workshop appointment for {service} service.
        
        Details of your reservation:
        Service: {service}
        Date: {date}
        Hour: {hour}
        
        If you have any question or need further assistance, feel free to contact us!
        
        Best Regards
        DnD Motorcycles Team 
        ''',
        from_email=settings.EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
