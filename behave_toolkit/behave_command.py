import os
import subprocess

from .mixins.output_panel import OutputPanelMixin
from .mixins.steps import StepsMixin


class BehaveCommand(OutputPanelMixin,
                    StepsMixin):

    '''
    Base class for all Sublime commands that interact with behave
    '''

    def behave(self, *args, **kwargs):
        '''
        Run the behave command specified in `*args` and return the output
        of the git command as a string. If output=True, the output will be
        shown live in an output panel.
        '''

        command = (self.python_binary_path, ) + \
            tuple(behave for behave in self.behave_binary_path) + \
            tuple(arg for arg in args if arg)

        stdout = ''
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              cwd=self.view.window().folders()[0]) as p:

            # Premature optimization is the root of all evil
            # But this could be more DRY
            if kwargs.get('output', False):
                self.erase()
                for line in p.stdout:
                    stdout += line
                    self.append(line, end='')

            else:
                for line in p.stdout:
                    stdout += line

        return stdout

    @property
    def behave_binary_path(self):
        '''
        Return the path to the `behave` binary in tuple form. This is because
        `behave_command` may not be a single binary. (e.g. manage.py behave)
        '''
        behave = self.view.settings().get('behave_command')

        if behave:
            if type(behave) == list:
                return behave
            else:
                return [behave]
        else:
            # default
            return [os.path.join(os.path.dirname(self.python_binary_path),
                                 'behave')]

    @property
    def python_binary_path(self):
        '''
        Return the path to the `python` binary.
        '''
        return self.view.settings().get('python_interpreter', 'python')
