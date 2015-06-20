import os
import subprocess

import sublime
import sublime_plugin

from ..utils.log import OutputPanelMixin


class BstRunScenario(sublime_plugin.TextCommand, OutputPanelMixin):

    def run(self, edit, **kwargs):
        current_line_number = self.view.rowcol(
            self.view.sel()[0].begin())[0] + 1
        sublime.status_message('Line number: %d' % current_line_number)
        python = self.view.settings().get('python_interpreter', 'python')

        behave = os.path.join(os.path.dirname(python), 'behave')

        with subprocess.Popen([python, behave],
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              cwd=self.view.window().folders()[0]) as p:
            for line in p.stdout:
                self.append(edit, line, end='')

            self.append(edit, 'Exit code: %d' % p.wait())

        # self.append(edit, 'Helloffffsdfsdfsdfsdfsdfsdfsfsdfsdfsdf')
        # self.append(edit, 'Number 2')
