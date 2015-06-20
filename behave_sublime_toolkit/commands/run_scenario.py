import sublime
import sublime_plugin

from ..utils.log import OutputPanelMixin


class BstRunScenario(sublime_plugin.TextCommand, OutputPanelMixin):

    def run(self, edit, **kwargs):
        current_line_number = self.view.rowcol(
            self.view.sel()[0].begin())[0] + 1
        sublime.status_message('Line number: %d' % current_line_number)
        python = self.view.settings().get('python_interpreter', 'python')

        self.append(edit, 'Helloffffsdfsdfsdfsdfsdfsdfsfsdfsdfsdf')
        self.append(edit, 'Number 2')
