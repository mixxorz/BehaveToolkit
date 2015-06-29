import os

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand
from ..utils import parser
from ..utils.scope import is_gherkin
from ..utils.text import snake_caseify


STEP_SNIPPET = '''
@${type}(u'${name}')
def ${func}(context):
    raise NotImplementedError(u'STEP: ${name}')

'''


class BtGenerateStepFunction(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Generates step function(s) for steps under the cursor(s).
    '''

    def run(self, edit, line_numbers=None):
        sublime.set_timeout_async(
            lambda: self.run_async(line_numbers=line_numbers))

    def run_async(self, line_numbers):
        # Set line_numbers of the steps we're generating
        self.line_numbers = line_numbers

        # If nothing was passed in, load it from the current view
        if not self.line_numbers:
            self.line_numbers = []
            for region in self.view.sel():
                self.line_numbers.append(
                    self.view.rowcol(region.begin())[0] + 1)

        step_data = self._get_step_data()

        used_steps = parser.parse_used_steps(step_data)
        unused_steps = parser.parse_unused_steps(step_data)
        unimplemented_steps = parser.parse_unimplemented_steps(step_data)

        # Selected steps is a set of Usages that were under the cursors
        self.selected_steps = self._get_selected_steps(unimplemented_steps)

        # TODO: Should sort by most recently selected
        self.step_file_paths = self._get_step_file_paths(used_steps,
                                                         unused_steps)
        items = [['Create a new file',
                  'Creates a new file with the step function.']]
        items += [[os.path.basename(dir), dir]
                  for dir in self.step_file_paths]

        self.view.window().show_quick_panel(items,
                                            self.on_select_action)

    def on_select_action(self, selected_index):
        '''
        Triggers on select from quick panel.
        '''

        if selected_index == -1:
            return

        # Create new file
        elif selected_index == 0:
            # TODO: Set Syntax of the new file to be python
            view = self.view.window().new_file()

            # Append snippet to the view
            sublime.set_timeout(
                lambda: self._append_snippet(view, new=True), 10)

        # Select existing file
        else:
            # Subtract one to account for the "Create file" item
            directory_index = selected_index - 1

            current_root = self.view.window().folders()[0]

            # The paths are relative to the project root
            file_directory = os.path.join(
                current_root,
                self.step_file_paths[directory_index])
            view = self.view.window().open_file(file_directory)

            # Append snippet to the view
            sublime.set_timeout(lambda: self._append_snippet(view), 10)

    def _append_snippet(self, view, new=False):
        '''
        Append snippet to the chosen file. If new=True, also set syntax to
        Python and add behave imports
        '''

        if view.is_loading():
            sublime.set_timeout(lambda: self._append_snippet(view), 10)
        else:
            snippet_buffer = ''

            # If it's a new file, add the behave imports
            if new:
                snippet_buffer += 'from behave import given, when, then\n\n'
            else:
                snippet_buffer += '\n'

            for usage in self.selected_steps:
                snippet = sublime.expand_variables(
                    STEP_SNIPPET,
                    {'type': usage.type,
                     'name': usage.name,
                     'func': snake_caseify(usage.name)})

                snippet_buffer += snippet

            initial_view_size = view.size()

            view.run_command('append', {'characters': snippet_buffer})

            # Scroll to bottom
            view.run_command('move_to', {'to': 'eof'})

            # Select the appended text
            view.sel().add(sublime.Region(initial_view_size, view.size()))

    def _get_step_file_paths(self, used_steps, unused_steps):
        """Get the path of the step files used by behave."""

        all_steps = used_steps + unused_steps

        step_file_paths = set()

        for step in all_steps:
            # Only list files within the project
            if step.path[:2] != '..':
                step_file_paths.add(step.path)

        return list(step_file_paths)

    def _get_selected_steps(self, unimplemented_steps):
        '''
        Get steps under the cursors as a set of namedtuples.

        The tuple is defined as:
        Step = namedtuple('Step', ['step_type', 'name'])
        '''

        current_root = self.view.window().folders()[0]
        current_file = os.path.relpath(self.view.file_name(), current_root)

        selected_steps = set()

        # Find the steps under the cursors
        for line_number in self.line_numbers:

            # Use the location to find the matching step
            # (e.g. features/toolkit.feature:4)
            location = '%s:%d' % (current_file, line_number)

            for usage in unimplemented_steps:

                step_location = '%s:%d' % (usage.path, usage.line)

                if step_location == location:
                    selected_steps.add(usage)
                    break

        return selected_steps

    def is_enabled(self):
        '''
        Enable only for Gherkin
        '''
        return is_gherkin(self.view)
