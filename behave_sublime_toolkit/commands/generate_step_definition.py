from collections import namedtuple
import json
import os
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand
from ..utils.text import snake_caseify


STEP_SNIPPET = '''
@${type}(u'${name}')
def ${func}(context):
    raise NotImplementedError(u'STEP: ${name}')

'''


class BstGenerateStepDefinition(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Generates step definition(s) for steps under the cursor(s).
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

        # Selected steps is a set of Steps that were under the cursors
        self.selected_steps = self._get_selected_steps()

        # TODO: Should sort by most recently selected
        self.step_file_paths = self._get_step_file_paths()
        items = [['Create a new file',
                  'Creates a new file with the step definition.']]
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
                snippet_buffer += 'from behave import given, when, then\n'
            else:
                snippet_buffer += '\n'

            for step in self.selected_steps:
                snippet = sublime.expand_variables(
                    STEP_SNIPPET,
                    {'type': step.step_type,
                     'name': step.name,
                     'func': snake_caseify(step.name)
                     .replace(' ', '_')})

                snippet_buffer += snippet

            initial_view_size = view.size()

            view.run_command('append', {'characters': snippet_buffer})

            # Scroll to bottom
            view.run_command('move_to', {'to': 'eof'})

            # Select the appended text
            view.sel().add(sublime.Region(initial_view_size, view.size()))

    def _get_step_file_paths(self):
        '''
        Get the path of the step files used by behave.
        '''

        output = self.behave('--dry-run',
                             '--format',
                             'steps.doc',
                             '--no-summary',
                             '--no-snippets')

        p = re.compile('Location:\s(.*):\d+', re.MULTILINE)

        matched_set = re.findall(p, output)

        step_file_paths = list(set(matched_set))

        # Since all the directories returned by behave are relative to the
        # project root, anything that starts with '..' is outside the project's
        # scope. We don't want to list those
        step_file_paths = [
            dir for dir in step_file_paths if not dir[:2] == '..']

        return step_file_paths

    def _get_selected_steps(self):
        '''
        Get steps under the cursors as a set of namedtuples.

        The tuple is defined as:
        Step = namedtuple('Step', ['step_type', 'name'])
        '''

        current_root = self.view.window().folders()[0]
        current_file = os.path.relpath(self.view.file_name(), current_root)

        # Query behave for step information
        json_output = self.behave(current_file, '--dry-run',
                                  '--format', 'json', '--no-summary',
                                  '--no-snippets')
        output = json.loads(json_output)

        # Get all the steps
        all_steps = []

        for feature in output:
            for element in feature['elements']:
                for step in element['steps']:
                    all_steps.append(step)

        Step = namedtuple('Step', ['step_type', 'name'])

        selected_steps = set()

        # Find the steps under the cursors
        for line_number in self.line_numbers:

            # Use the location to find the matching step
            # (e.g. features/toolkit.feature:4)
            location = '%s:%d' % (current_file, line_number)

            for step in all_steps:
                if step['location'] == location:
                    selected_steps.add(Step(step['step_type'], step['name']))
                    break

        return selected_steps
