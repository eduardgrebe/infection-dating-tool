from django.conf import settings
from django.core.urlresolvers import reverse

def update_email_context(context):

    context['site_base_url'] = settings.SITE_BASE_URL
    context['base_url'] = settings.BASE_URL
    context['mailto_url'] = settings.MAIL_TO
    
    # context['account_orders_url'] = u'%s%s' % (settings.BASE_URL,
    #                                            reverse('account_orders'))
    # context['account_billing_url'] = u'%s%s' % (settings.BASE_URL,
    #                                            reverse('account_billing'))
    # context['account_invite_url'] = u'%s%s' % (settings.BASE_URL,
    #                                            reverse('account_invite'))

    # context['contact_url'] = u'%s%s' % (settings.BASE_URL,
    #                                     reverse('wordpress',
    #                                     kwargs={'wp_url': 'contactus'}))

    # context['faq_url'] = u'%s%s' % (settings.BASE_URL,
    #                                 reverse('wordpress',
    #                                 kwargs={'wp_url': 'faq'}))
        
    # context['facebook'] = settings.FACEBOOK_LINK
    # context['instagram'] = settings.INSTAGRAM_LINK
    # context['twitter'] = settings.TWITTER_LINK
    return context
