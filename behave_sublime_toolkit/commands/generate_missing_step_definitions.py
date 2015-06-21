import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstGenerateMissingStepDefinitions(sublime_plugin.TextCommand,
                                        BehaveCommand):

    def run(self, edit):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):

        undefined_steps = self.get_undefined_steps()

        self.view.run_command(
            'bst_generate_step_definition',
            {'line_numbers': [step.line for step in undefined_steps]})
