import os

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand
from ..utils import parser
from ..utils.scope import is_gherkin


class BstGoToStepDefinition(sublime_plugin.TextCommand, BehaveCommand):
    """Go to step definition for the step under the cursor"""

    def run(self, edit):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):
        # TODO: Maybe extract this functionality to a mixin
        current_root = self.view.window().folders()[0]
        current_file = os.path.relpath(self.view.file_name(), current_root)
        current_line_number = self.view.rowcol(
            self.view.sel()[0].begin())[0] + 1

        query_location = '%s:%s' % (current_file, current_line_number)

        step_data = self._get_step_data()

        used_steps = parser.parse_used_steps(step_data)
        unused_steps = parser.parse_unused_steps(step_data)

        all_steps = used_steps + unused_steps

        matched_step = None
        for step in all_steps:
            if matched_step:
                break
            for usage in step.usages:
                usage_location = '%s:%d' % (usage.path, usage.line)
                if usage_location == query_location:
                    matched_step = step
                    break

        if matched_step:
            absolute_path = os.path.join(
                current_root,
                matched_step.path)

            absolute_path += ':%d' % matched_step.line

            self.view.window().open_file(absolute_path,
                                         sublime.ENCODED_POSITION)
        else:
            sublime.status_message(
                'Definition not found for: "%s"' % query_location)

    def is_enabled(self):
        """Enable only for Gherkin"""
        return is_gherkin(self.view)
