import pandas as pd
from django.utils import timezone
from rental.views.utils import get_unavailable_dates
from workshop.views.utils import get_unavailable_hours


def get_unavailable_dates_dict(reservations):
    """
    Returns a dictionary mapping motorcycles to their unavailable dates based on existing reservations.

    :param reservations: List of reservation objects.

    :return:
        dict: A dictionary where keys are motorcycles and values are lists of unavailable dates.
    """
    unavailable_dates_dict = {}
    for reservation in reservations:
        motorcycle = reservation.motorcycle
        unavailable_dates = get_unavailable_dates(motorcycle)
        user_reservation_date_range = pd.date_range(reservation.start_date, reservation.end_date)
        user_reservation = [d.strftime('%Y-%m-%d') for d in user_reservation_date_range]
        dates_without_user_reservations = [date for date in unavailable_dates if date not in user_reservation]

        unavailable_dates_dict[motorcycle] = dates_without_user_reservations

    return unavailable_dates_dict


def get_unavailable_hours_dict(reservations):
    """
     Returns a dictionary mapping services to their unavailable hours based on existing reservations.

     :param reservations: List of reservation objects.

     :return:
        dict: A dictionary where keys are services and values are dictionaries
        mapping dates to lists of unavailable hours.
     """
    unavailable_hours_dict = {}
    for reservation in reservations:
        service = reservation.service
        unavailable_hours = get_unavailable_hours(reservation.service.slug)
        user_service_reservation = timezone.template_localtime(reservation.date_time).time().strftime('%I:%M %p')

        hours_without_user_reservation = {
            k: v for (k, v) in unavailable_hours.items() if user_service_reservation not in v
        }

        print(hours_without_user_reservation)
        unavailable_hours_dict[service] = hours_without_user_reservation

    return unavailable_hours_dict
