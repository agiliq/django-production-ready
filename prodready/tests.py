import os
from django.test import TestCase

from prodready.management.commands.is_it_ready import Validations


class ValidationsTest(TestCase):

    def run_validations(self, method_name):
        validations = Validations()
        messages = getattr(validations, method_name)()
        return messages
        
    def test_debug(self):
        """
        Tests that `messages` is populated when settings.DEBUG is True
        """
        with self.settings(DEBUG=True):
            messages = self.run_validations('check_debug_values')
            self.assertIn('Set DEBUG to False', messages)

        with self.settings(DEBUG=False):
            messages = self.run_validations('check_debug_values')
            self.assertNotIn('Set DEBUG to False', messages)
    
    def test_contacts(self):
        """
        Tests that `messages` is populated when settings.ADMINS are empty
        """
        messages = self.run_validations('check_contacts')
        self.assertIn('Enter valid email address in ADMINS section', messages)

        with self.settings(ADMINS=('test@mail.com',)):
            messages = self.run_validations('check_contacts')
            self.assertNotIn('Enter valid email address in ADMINS section', messages)
        
        messages = self.run_validations('check_contacts')
        self.assertIn('Enter valid email address in MANAGERS section', messages)

        with self.settings(MANAGERS=('test@mail.com',)):
            messages = self.run_validations('check_contacts')
            self.assertNotIn('Enter valid email address in MANAGERS section', messages)

    def test_email(self):
        """
        Tests that `messages` is populated when settings.EMAILS are default
        """
        messages = self.run_validations('check_email')
        self.assertIn('Setup E-mail host', messages)

        with self.settings(EMAIL_HOST_USER='test'):
            messages = self.run_validations('check_email')
            self.assertNotIn('Setup E-mail host', messages)

        messages = self.run_validations('check_email')
        self.assertIn('Set a valid email for SERVER_EMAIL',messages)

        with self.settings(SERVER_EMAIL='test@localhost'):
            messages = self.run_validations('check_email')
            self.assertNotIn('Set a valid email for SERVER_EMAIL',messages)
        
        messages = self.run_validations('check_email')
        self.assertIn('Set a valid email for DEFAULT_FROM_EMAIL',messages)

        with self.settings(DEFAULT_FROM_EMAIL='test@localhost'):
            messages = self.run_validations('check_email')
            self.assertNotIn('Set a valid email for DEFAULT_FROM_EMAIL',messages)
    
    def test_default_templates(self):
        """
        Tests that `messages` is populated when DEFAULT_TEMPLATES does not exist
        """
        messages = self.run_validations('check_default_templates')
        self.assertIn('Template 404.html does not exist', messages)
        self.assertIn('Template 500.html does not exist', messages)

        with self.settings(TEMPLATE_DIRS = (os.path.abspath('test_dir'),)):
            messages = self.run_validations('check_default_templates')
            self.assertNotIn('Template 404.html does not exist', messages)
            self.assertNotIn('Template 500.html does not exist', messages)