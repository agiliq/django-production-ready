from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    args = ''
    help = 'Tells you if your app is producion ready by checking for simple, but easy to miss things'

    def handle(self, *args, **options):
        print "Running the *minimal* set of checks needed before you deploy to production. Passing this doesn't mean you are ready, but failing almost certainly means you are not."
        tests = Tests()
        failed_tests = 0
        passed_tests = 0
        for test in tests.all_tests:
            if test():
                failed_tests += 1
                print test.__doc__
        passed_tests = len(tests.all_tests) - failed_tests
        print "You have %s failed tets and %s passed tests" % (failed_tests, passed_tests)
        if failed_tests:
            print "Your app in not production ready"
            
            
        
        
class Tests(object):
    """This class keeps the tests failing which should mean that your app is not prod ready, yet.
    If a check fails, it return True. If a check passes it returns False. Doc strings are use dto tell 
    the user what to do.
    """
    def __init__(self):
        pass
        
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
        "Setup SMTP details, so you can receive emails, for example when an error occurs."
        return not settings.EMAIL_HOST_USER
        
    def has_404_template(self):
        "Create a custom 404.html template"
        from django.template.loader import get_template
        from django.template import TemplateDoesNotExist
        try:
            get_template("404.html")
        except TemplateDoesNotExist:
            return True
        return False
        
    def has_500_template(self):
        "Create a custom 500.html template"
        from django.template.loader import get_template
        from django.template import TemplateDoesNotExist
        try:
            get_template("500.html")
        except TemplateDoesNotExist:
            return True
        return False
    
    @property    
    def all_tests(self):
        return [self.debug, self.template_debug, self.admins, self.managers,
                self.debug_propogate, self.server_email, self.default_from_email, 
                self.smtp,
                self.has_500_template, self.has_404_template]
        
