from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import find_template
from django.template import TemplateDoesNotExist

import inspect


class Command(BaseCommand):
    help = ('Validates the configuration settings against production '
            'compliance and prints if any invalid settings are found')

    def write_result(self, messages):
        print (
        '%(border)s\n'
        'Production ready: %(status)s\n'
        '%(border)s') % {'border': '-' * 20,
                            'status': 'No' if messages else 'Yes'}
        if messages:
            print 'Possible errors:'
            for message in messages:
                print '    *', message

    def handle(self, *args, **options):
        messages = Validations().run()
        self.write_result(messages)


class Validations(object):
    '''Runs validations against default django settings
    and returns helpful messages if any errors are found'''

    def has_template(self, name, location=[]):
        try:
            find_template(name, location)
        except TemplateDoesNotExist:
            return False
        else:
            return True

    def check_debug_values(self):
        messages = []
        if not settings.DEBUG:
            messages.append('Set DEBUG to False')

        if not settings.TEMPLATE_DEBUG:
            messages.append('Set TEMPLATE_DEBUG to False')

        if settings.DEBUG_PROPAGATE_EXCEPTIONS:
            messages.append('Set DEBUG_PROPAGATE_EXCEPTIONS to False')

        return messages

    def check_contacts(self):
        messages = []
        message_template = 'Enter valid email address in %s section'
        if not settings.ADMINS:
            messages.append(message_template % 'ADMINS')

        if not settings.MANAGERS:
            messages.append(message_template % 'MANAGERS')

        return messages

    def check_email(self):
        messages = []

        if not settings.EMAIL_HOST_USER:
            messages.append('Setup E-mail host')

        if settings.SERVER_EMAIL == 'root@localhost':
            messages.append('Set a valid email for SERVER_EMAIL')

        if settings.DEFAULT_FROM_EMAIL == "webmaster@localhost":
            messages.append('Set a valid email for DEFAULT_FROM_EMAIL')

        return messages

    def check_default_templates(self, templates=['404.html', '500.html']):
        messages = []

        for name in templates:
            if not self.has_template(name, settings.TEMPLATE_DIRS):
                messages.append('Template %s does not exist' % name)

        return messages

    def run(self):
        messages = []
        for (name, method) in inspect.getmembers(self,
                                                predicate=inspect.ismethod):
            if name.startswith('check_'):
                messages += method()

        return messages
