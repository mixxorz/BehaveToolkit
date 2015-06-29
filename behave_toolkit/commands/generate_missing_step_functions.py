import sublime
import sublime_plugin

from ..behave_command import BehaveCommand
from ..utils.scope import is_gherkin


class BtGenerateMissingStepFunctions(sublime_plugin.TextCommand,
                                     BehaveCommand):

    """Generates step functions for unimplemented steps."""

    def run(self, edit):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):

        unimplemented_steps = self.get_unimplemented_steps()

        self.view.run_command(
            'bt_generate_step_function',
            {'line_numbers': [step.line for step in unimplemented_steps]})

    def is_enabled(self):
        """Enabled only for Gherkin."""
        return is_gherkin(self.view)
