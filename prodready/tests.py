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
