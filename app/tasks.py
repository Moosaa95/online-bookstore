from django.core import mail
from background_task import background

@background(schedule=1)  # Adjust the schedule as needed
def send_activation_email(recipient_list, subject, html_message, from_email):
    try:
        recipient_list = [recipient_list]
        mail.send_mail(subject, html_message, from_email, recipient_list)
    except Exception as e:
        # Handle email sending failure here
        print(f"Email sending failed: {e}")