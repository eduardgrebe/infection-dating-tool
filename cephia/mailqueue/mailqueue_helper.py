""" One-stop functions for sending emails from anywhere in the project """

import logging
from django.utils import timezone
logger = logging.getLogger(__name__)
from datetime import datetime
from django.template import RequestContext, Context
from django.db import transaction
from models import MailerMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files import File
from django.core.files.base import ContentFile
import datetime
from django.core.mail import send_mail

def queue_admin_email(subject, msg, supplementary_to_addresses=None):
    return queue_email(subject_content=subject, text_content="%s\n\n%s" % (subject,msg),
                       html_content="%s<br/><br/>%s" % (subject,msg),
                       to_addresses=settings.MAIL_ADMINS + (supplementary_to_addresses or []))


def queue_templated_email(request, context, subject_template, text_template, html_template, to_addresses, from_address, 
                          bcc_addresses=None, attachments=None, inline_attachments=None):
    """ will render the templates against the request and context, and then queue the email.

        returns a MailMessage object, onto which you can put the
        attachments instead of using the attachments parameter if you prefer
    """

    bcc_addresses = bcc_addresses or []
    try:
        if settings.EMAIL_TEST_MODE:
            to_addresses = settings.MAIL_ADMINS
    except AttributeError:
        pass
    
    context['WEB_URL'] = settings.BASE_URL
    context['STATIC_URL'] = settings.BASE_URL + settings.STATIC_URL
    context['settings'] = settings
    
    if request is None:
        request_context = Context(context)
    else:
        request_context = RequestContext(request, context)
    #subject_content = render_to_string(subject_template, request_context)
    subject_content = subject_template
    text_content = render_to_string(text_template, request_context)
    html_content = render_to_string(html_template, request_context)
    return queue_email(
        subject_content, text_content, html_content, to_addresses, from_address,
        bcc_addresses, attachments, inline_attachments=inline_attachments)

def queue_email(subject_content, text_content, html_content, to_addresses, from_address=None,
                bcc_addresses=None, attachments=None, inline_attachments=None):

    msg = MailerMessage(html_content=html_content, from_address=from_address or settings.FROM_EMAIL, to_address=",".join(to_addresses),)

    send_mail(
        subject=subject_content,
        message=text_content,
        from_email=msg.from_address,
        recipient_list=[msg.to_address],
        fail_silently=False,
        auth_user=None,
        auth_password=None,
        connection=None,
        html_message=msg.html_content
    )

    # msg = MailerMessage(
    #     subject=subject_content,
    #     content=text_content,
    #     html_content=html_content,
    #     to_address=",".join(to_addresses),
    #     bcc_address=",".join(bcc_addresses or []),
    #     from_address=from_address or settings.FROM_EMAIL,
    #     app='infection_dating_tool',
    #     created=timezone.now()
    #     )
    # logger.debug(msg, msg.to_address)

    # if attachments:
    #     for f, filename in attachments:
    #         if not isinstance(f, File):
    #             f = ContentFile(f)
    #         msg.add_attachment(f, filename)

    # if inline_attachments:
    #     for f, filename, content_id in inline_attachments:
    #         if not isinstance(f, File):
    #             f = ContentFile(f)
    #         msg.add_attachment(f, filename, content_id)

    # recipient_list = [msg.to_address]
    # send_mail(subject=msg.subject, message=msg.content, from_email=msg.from_address, recipient_list=recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=msg.html_content)
    # # msg.save()
    # return msg
