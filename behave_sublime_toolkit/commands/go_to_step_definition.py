import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstGoToStepDefinition(sublime_plugin.TextCommand, BehaveCommand):

    def run(self, edit):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):
        pass
