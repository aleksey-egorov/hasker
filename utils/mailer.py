import re
import logging

from django.core.mail import send_mail
from django.conf import settings

class Mailer():

    def send(self, email, alias, context):
        logger = logging.getLogger(__name__)
        try:
            msg = settings.EMAIL_MESSAGES[alias]
            subject = msg[0]
            message = self.replace_context(msg[1], context) + settings.EMAIL_SIGN
            send_mail(subject, message=' ', html_message=message,
                from_email=settings.EMAIL_FROM, recipient_list=[email],
                fail_silently=False,
            )
            return message
        except Exception as err:
            logger.error(err)

    def replace_context(self, msg, context):
        if isinstance(context, dict):
            for key in context.keys():
                tag = '<%' + str(key).upper() + '%>'
                msg = re.sub(tag, context[key], msg)

        return msg