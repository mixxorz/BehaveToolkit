import os
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstGenerateStepDefinition(sublime_plugin.TextCommand, BehaveCommand):

    def run(self, edit, **kwargs):
        self.snippet = self._generate_snippet(
            '\n\nI AM SOME STEP ==========================')

        # TODO: Should sort by most recently selected
        self.step_directories = self._get_step_directories()
        items = [['Create a new file',
                  'Creates a new file with the step definition.']]
        items += [[os.path.basename(dir), dir]
                  for dir in self.step_directories]

        self.view.window().show_quick_panel(items,
                                            self.on_select_action)

    def on_select_action(self, selected_index):
        # Create new file
        if selected_index == -1:
            return
        elif selected_index == 0:
            view = self.view.window().new_file()

            # TODO: Add behave imports to the new file (by editing the snippet
            # maybe)
        # Select existing file
        else:
            # Subtract one to account for the "Create file" item
            directory_index = selected_index - 1

            view = self.view.window().open_file(
                self.step_directories[directory_index])

        # Append snippet to the view
        sublime.set_timeout(lambda: self._append_snippet(view), 10)

    def _append_snippet(self, view):
        if view.is_loading():
            sublime.set_timeout(lambda: self._append_snippet(view), 10)
        else:
            view.run_command('append', {'characters': self.snippet,
                                        'scroll_to_end': True})

    def _get_step_directories(self):
        # TODO: Should not include files that are outside the project's scope
        output = self.behave('--dry-run',
                             '--format',
                             'steps.doc',
                             '--no-summary',
                             '--no-snippets')

        p = re.compile('Location:\s(.*):\d+', re.MULTILINE)

        matched_set = re.findall(p, output)

        step_directories = list(set(matched_set))

        return step_directories

    def _generate_snippet(self, step):
        return step
