from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        tests = Tests()
        failed_tests = 0
        passed_tests = 0
        for test in tests.all_tests:
            if test:
                failed_tests += 1
                print test.__doc__
        passed_tests = len(tests.all_tests) - failed_tests
        print "You have %s failed tets and %s passed tests" % (failed_tests, passed_tests)
        if failed_tests:
            print "Your app in not production ready"
            
            
        
        
class Tests(object):
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
        return settings.ADMINS
        
    def managers(self):
            "Enter your email address in MANAGERS to receive error emails"
            return settings.ADMINS
            
    def debug_propogate(self):
        "Set DEBUG_PROPAGATE_EXCEPTIONS to False"
        return settings.DEBUG_PROPAGATE_EXCEPTIONS
        
    def server_email(self):
        "Set a valid email as SERVER_EMAIL"
        settings.SERVER_EMAIL == "root@localhost"
        
    def default_from_email(self):
        "Set a valid email as DEFAULT_FROM_EMAIL"
        settings.DEFAULT_FROM_EMAIL == "webmatser@localhost"
        
    
    @property    
    def all_tests(self):
        return [self.debug, self.template_debug, self.admins, self.managers,
                self.debug_propogate, server_email, default_from_email]
        
