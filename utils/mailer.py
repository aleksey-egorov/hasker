import re

from django.core.mail import send_mail
from django.conf import settings

class Mailer():

    def send(self, email, alias, context):
        try:
            msg = settings.EMAIL_MESSAGES[alias]
            subject = msg[0]
            message = self.replace_context(msg[1], context) + settings.EMAIL_SIGN
            send_mail(subject, message=' ', html_message=message,
                from_email=settings.EMAIL_FROM, recipient_list=[email],
                fail_silently=False,
            )
            return message
        except:
            pass

    def replace_context(self, msg, context):
        if isinstance(context, dict):
            for key in context.keys():
                tag = '<%' + str(key).upper() + '%>'
                msg = re.sub(tag, context[key], msg)

        return msg