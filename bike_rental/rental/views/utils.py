import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from rental.models import MotorcycleReservation


def get_unavailable_dates(motorcycle):
    """
    Returns a list of unavailable dates for a specific motorcycle based on its reservations.

    :param motorcycle: Motorcycle object.
    :return: List of dates in 'YYY-MM-DD' format.
    """
    reservations = MotorcycleReservation.objects.filter(motorcycle=motorcycle)

    start_date = [r.start_date for r in reservations]
    end_date = [r.end_date for r in reservations]

    unavailable_dates = []

    for start, end in zip(start_date, end_date):
        pd_date_range = pd.date_range(start, end)

        date_range = [d.strftime('%Y-%m-%d') for d in pd_date_range]
        unavailable_dates += date_range

    return unavailable_dates


def send_confirmation_mail(user, motorcycle, start_date, end_date, date_range):
    """
     Sends a confirmation email with reservation details and total price to the user.
     Calculates the total price based on the rental period.

     :param user: The user making the reservation.
     :param motorcycle: The reserved motorcycle.
     :param start_date: The start date of the reservation.
     :param end_date: The end date of the reservation.
     :param date_range: List of dates included in the reservation.

     Note:
     The price is calculated based on the number of rental days and potential discounts.
     """
    days = len(date_range)
    price = None

    if days <= 3:
        price = float(motorcycle.rental_price) * days
    elif 4 <= days <= 7:
        price = (float(motorcycle.rental_price) * 0.95) * days
    elif 8 <= days <= 100:
        price = (float(motorcycle.rental_price) * 0.9) * days

    send_mail(
        subject='Confirm reservation',
        message=f'''
        Dear {user.first_name},

        We are delighted to confirm your reservation for {motorcycle}.

        Details of your reservation:
        Motorcycle: {motorcycle}
        Start Date: {start_date}
        End Date: {end_date}
        
        Total price: {price} $
        
        If you have any question or need further assistance, feel free to contact us! 

        Best Regards
        DnD Motorcycles Team
        ''',
        from_email=settings.EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def recently_viewed(request, motorcycle_id):
    """Manages a session-based list of recently viewed motorcycle IDs. Takes 'request' and 'motorcycle_id' as
    parameters. Checks and updates the list to track last viewed motorcycles. Limits the list to a maximum
    of 3 elements to store the latest views."""
    if 'recently_viewed' not in request.session:
        request.session['recently_viewed'] = []
        request.session['recently_viewed'].append(motorcycle_id)

    else:
        if motorcycle_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(motorcycle_id)

        request.session['recently_viewed'].insert(0, motorcycle_id)

        if len(request.session['recently_viewed']) > 4:
            request.session['recently_viewed'].pop()

    request.session.modified = True
