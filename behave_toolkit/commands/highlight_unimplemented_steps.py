import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BtHighlightUnimplementedSteps(sublime_plugin.TextCommand, BehaveCommand):

    """Highlights unimplemented steps in a feature file."""

    REGION_NAME = 'bt.unimplemented_steps'

    def run(self, edit, **kwargs):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):

        unimplemented_steps = self.get_unimplemented_steps()

        regions = []

        for step in unimplemented_steps:
            matched_regions = self.view.find_all(
                '%s %s' % (step.keyword, step.name))
            regions += matched_regions

        self.view.add_regions(self.REGION_NAME, regions, 'comment')
