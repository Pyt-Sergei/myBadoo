from django.core.mail import send_mail
from smtplib import SMTPException


def email_send(subject, message, recipient_list, from_email=None):
    # try:
    #     send_mail(subject, message, from_email, recipient_list)
    # except SMTPException:
    #     return {'error': "Email wasn't sent"}
    # else:
    #     return False
    send_mail(subject, message, from_email, recipient_list)
    return False
