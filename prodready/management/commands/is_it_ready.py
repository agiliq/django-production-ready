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
        messages = Validations().run(options)
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

    def check_print_statement(self):
        import ast
        import os
        linenos = []
        linenos_list = []

        class PrintStatementFinder(ast.NodeVisitor):
            def visit_Print(self, node):
                if node.dest is None:
                    linenos_list.append(node.values[0].lineno)

        for (path, dirs, files) in os.walk("."):
            for file_name in files:
                if file_name.endswith(".py"):
                    with open(path + "/" + file_name, 'rU') as f:
                        linenos_list = []
                        PrintStatementFinder().visit(ast.parse("".join(f.readlines())))
                        if linenos_list:
                            linenos.append(path + "/" + file_name)
                            linenos.append(linenos_list)
        if linenos:
            if self.verbosity >= '2':
                return ["There are print statements  'filename' , [list of linenos of  print statements in the file ] ", linenos]
            else:
                return ["You have one or more print statements"]
        else:
            return []

    def check_ipdb_import(self):
        import ast
        import os
        linenos = []
        linenos_list = []

        class ImportIpdbFinder(ast.NodeVisitor):
            def visit_Import(self, node):
                for names in node.names:
                    if names.name == "ipdb" or  names.name == "pdb":
                        linenos_list.append(node.lineno)

            def visit_ImportFrom(self, node):
                if node.names[0].name == "set_trace":
                    linenos_list.append(node.lineno)

        for (path, dirs, files) in os.walk("."):
            for file_name in files:
                if file_name.endswith(".py"):
                    with open(path + "/" + file_name, 'rU') as f:
                        linenos_list = []
                        ImportIpdbFinder().visit(ast.parse("".join(f.readlines())))
                        if linenos_list:
                            linenos.append(path + "/" + file_name)
                            linenos.append(linenos_list)
        if linenos:
            if self.verbosity >= '2':
                return ["There are ipdb imports   'filename' , [list of linenos of  ipdb import  statements in the file ] ", linenos]
            else:
                return ["You have one or more ipdb import  statements"]
        else:
            return []

    def run(self, options=None):
        self.verbosity = options['verbosity']
        messages = []
        for (name, method) in inspect.getmembers(self,
                                                predicate=inspect.ismethod):
            if name.startswith('check_'):
                messages += method()

        return messages
