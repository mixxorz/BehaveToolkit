import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstHighlightUndefinedSteps(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Highlights undefined steps in a feature file.

    This command uses the 'steps.usage' format and parses its output to
    get the undefined steps.
    '''

    REGION_NAME = 'bst.undefined_steps'

    def run(self, edit, **kwargs):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):

        undefined_steps = self.get_undefined_steps()

        regions = [self.view.find(step.name, 0) for step in undefined_steps]

        self.view.add_regions(self.REGION_NAME, regions, 'comment')