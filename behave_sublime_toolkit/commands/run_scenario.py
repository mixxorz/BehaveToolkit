import os
import subprocess

import sublime
import sublime_plugin

from ..utils.log import OutputPanelMixin


class BstRunScenario(sublime_plugin.TextCommand, OutputPanelMixin):

    '''
    Runs the behave scenario under the cursor
    '''

    def run(self, edit, **kwargs):
        args = []

        python = self.view.settings().get('python_interpreter', 'python')
        args.append(python)

        behave = os.path.join(os.path.dirname(python), 'behave')
        args.append(behave)

        if 'gherkin' in self.view.scope_name(0):
            current_file = self.view.file_name()
            current_line_number = self.view.rowcol(
                self.view.sel()[0].begin())[0] + 1

            scenario = '%s:%d' % (current_file, current_line_number)
            args.append(scenario)

        with subprocess.Popen(args,
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              cwd=self.view.window().folders()[0]) as p:
            for line in p.stdout:
                self.append(edit, line, end='')

            self.append(edit, 'Exit code: %d' % p.wait())
