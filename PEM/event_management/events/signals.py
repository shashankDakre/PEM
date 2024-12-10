from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Bookings
from django.conf import settings

@receiver(post_save, sender=Bookings)
def send_success_mail(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        booking_date = instance.booking_date
        quantity = instance.quantity
        total_price = instance.total_price
        location = instance.event.location

        # Email subject and message
        subject = "Thank You For Ticket Booking with Ayojan"
        message = (
            f"Dear {user.fullName},\n\n"
            f"Thank you for Booking a {event.title} with us!\n\n"
            f"Here are your Booking details:\n"
            f"Event: {event.title}\n"
            f"Booking Date: {booking_date}\n" 
            f"Event Location: {location}\n"
            f"Number of Tickets: {quantity}\n"
            f"Total Price: ₹{total_price}\n\n"
            f"We hope you have a great experience!\n"
            f"Have a blast at Event!!!!\n\n"
            f"Best Regards,\n"
            f"Ayojan Team"
        )

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email
            [user.Email],  # Recipient's email
        )



