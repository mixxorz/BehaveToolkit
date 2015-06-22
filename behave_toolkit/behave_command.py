import subprocess

import sublime

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

        command = tuple(self.behave_command) + \
            tuple(arg for arg in args if arg)

        print('Command %s' % (command,))

        stdout = ''
        stderr = ''
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
                stdout, stderr = p.communicate()

        if stderr:
            print('STDERR: %s' % stderr)
        return stdout

    @property
    def behave_command(self):
        '''
        The command used to launch behave. This can be set by modifying the
        behave_command setting. The setting should be a list. If not set, the
        plugin uses value of `which behave`.
        '''
        behave = self.view.settings().get('behave_command')

        if behave:
            return behave
        else:
            # Find the behave executable
            which = 'which'
            if sublime.platform() == 'windows':
                which = 'where'

            return [subprocess.check_output([which, 'behave']).strip()]
