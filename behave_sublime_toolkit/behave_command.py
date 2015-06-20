import os
import subprocess

from .utils.log import OutputPanelMixin


class BehaveCommand(OutputPanelMixin):

    '''
    Base class for all Sublime commands that interact with behave
    '''

    def behave(self, *args, **kwargs):
        '''
        Run the behave command specified in `*args` and return the output
        of the git command as a string. If output=True, the output will be
        shown live in an output panel.
        '''
        command = [self.python_binary_path,
                   self.behave_binary_path] + [arg for arg in args if arg]

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
        Return the path to the `behave` binary.
        '''
        return os.path.join(os.path.dirname(self.python_binary_path), 'behave')

    @property
    def python_binary_path(self):
        '''
        Return the path to the `python` binary.
        '''
        return self.view.settings().get('python_interpreter', 'python')
