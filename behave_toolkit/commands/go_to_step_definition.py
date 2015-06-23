import os
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand
from ..utils.scope import is_gherkin


class BstGoToStepDefinition(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Go to step definition for the step under the cursor.
    '''

    def run(self, edit):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):
        # TODO: Maybe extract this functionality to a mixin
        current_root = self.view.window().folders()[0]
        current_file = os.path.relpath(self.view.file_name(), current_root)
        current_line_number = self.view.rowcol(
            self.view.sel()[0].begin())[0] + 1

        step = '%s:%s' % (current_file, current_line_number)

        output = self.behave(self.view.file_name(),
                             '--dry-run',
                             '--format',
                             'steps.usage',
                             '--no-summary',
                             '--no-snippets')

        undefined_offset = output.find('UNDEFINED STEPS')
        offset = output.find(step)

        # If UNDEFINED STEPS is found, make sure we have a valid offset
        if undefined_offset != -1:
            if offset > undefined_offset or offset == -1:
                sublime.status_message('Definition not found for "%s"' % step)
                return

        output = output[:offset]

        p = re.compile('(^@.*)', re.MULTILINE)
        last_match = re.findall(p, output)[-1]
        m = re.search('^@.*#(.*)$', last_match)

        file_path = m.group(1).strip()

        absolute_path = os.path.join(
            current_root,
            file_path)

        self.view.window().open_file(
            absolute_path, sublime.ENCODED_POSITION)

        # TODO: Move the cursor position to highlight the step definition
        # better

    def is_enabled(self):
        '''
        Enable only for Gherkin
        '''
        return is_gherkin(self.view)
