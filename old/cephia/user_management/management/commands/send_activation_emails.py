from tendo import singleton
me = singleton.SingleInstance('send_activation_emails')

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

from user_management.utils import ApiSession

class Command(BaseCommand):
    help = "Send activation emails to all users"

    def handle(self, *args, **options):
        self.session = ApiSession(settings.CRON_USER, settings.CRON_USER_PASSWORD, False)

        users = self.session.get('users/unactivated_users')['data']['users']
        
        for user in users:
            context = {
                'user': user,
                'BASE_URL': settings.BASE_URL
            }
            html_content = render_to_string('user_management/emails/activate_account.html', context)
            text_content = render_to_string('user_management/emails/activate_account.txt', context)
            self.session.post('users/send_activation_email', {
                'html_content': html_content,
                'text_content': text_content,
                'subject': "Activate your account",
                'user_id': user['id'],
            })
            