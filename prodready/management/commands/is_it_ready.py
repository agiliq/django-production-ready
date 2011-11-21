from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist


class Command(BaseCommand):
    help = ('Tells you if your app is producion ready by checking for '
            'simple, but easy to miss things')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.failed_tests = []
        self.passed_tests = []

    def write_result(self):
        print 'Passed: %d, Failed: %d' % (len(self.passed_tests),
                                            len(self.failed_tests))
        if self.failed_tests:
            print 'Possible errors:'
            for test in self.failed_tests:
                print '*', test.__doc__

        print '-' * 20
        print 'Production ready: %s' % \
                ('No' if self.failed_tests else 'Yes')
        print '-' * 20

    def handle(self, *args, **options):
        print ("Running the *minimal* set of checks needed before you "
                "deploy to production. Passing this doesn't mean you are "
                "ready, but failing almost certainly means you are not.")
        tests = Tests()

        for test in tests.all_tests:
            if test():
                self.failed_tests.append(test)
            else:
                self.passed_tests.append(test)

        self.write_result()


class Tests(object):
    """This class keeps the tests failing which should mean that your app
    is not prod ready, yet. If a check fails, it return True. If a check
    passes it returns False. Doc strings are use dto tell the user what to do.
    """

    def has_template(self, name):
        try:
            get_template(name)
        except TemplateDoesNotExist:
            return True
        else:
            return False

    def debug(self):
        "Set DEBUG = False"
        return settings.DEBUG

    def template_debug(self):
        "Set TEMPLATE_DEBUG = False"
        return settings.TEMPLATE_DEBUG

    def admins(self):
        "Enter your email address in ADMINS to receive error emails"
        return not settings.ADMINS

    def managers(self):
        "Enter your email address in MANAGERS to receive error emails"
        return not settings.MANAGERS

    def debug_propogate(self):
        "Set DEBUG_PROPAGATE_EXCEPTIONS to False"
        return settings.DEBUG_PROPAGATE_EXCEPTIONS

    def server_email(self):
        "Set a valid email as SERVER_EMAIL"
        return settings.SERVER_EMAIL == "root@localhost"

    def default_from_email(self):
        "Set a valid email as DEFAULT_FROM_EMAIL"
        return settings.DEFAULT_FROM_EMAIL == "webmaster@localhost"

    def smtp(self):
        """Setup SMTP details, so you can receive emails, for example when
        an error occurs."""
        return not settings.EMAIL_HOST_USER

    def has_404_template(self):
        "Create a custom 404.html template"
        return self.has_template('404.html')

    def has_500_template(self):
        "Create a custom 500.html template"
        return self.has_template('505.html')

    @property
    def all_tests(self):
        return [self.debug, self.template_debug, self.admins, self.managers,
                self.debug_propogate, self.server_email,
                self.default_from_email, self.smtp,
                self.has_500_template, self.has_404_template]
