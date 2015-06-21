from collections import namedtuple
import json
import os
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


STEP_SNIPPET = '''
@${type}(u'${name}')
def ${func}(context):
    raise NotImplementedError(u'STEP: ${name}')

'''


class BstGenerateStepDefinition(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Generates step definition(s) for steps under the cursor(s).
    '''

    def run(self, edit, **kwargs):

        # Selected steps is a set of Steps that were under the cursors
        self.selected_steps = self._get_selected_steps()

        # TODO: Should sort by most recently selected
        self.step_directories = self._get_step_directories()
        items = [['Create a new file',
                  'Creates a new file with the step definition.']]
        items += [[os.path.basename(dir), dir]
                  for dir in self.step_directories]

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
            # TODO: Add behave imports to the new file (by editing the snippet
            # maybe)
            view = self.view.window().new_file()

        # Select existing file
        else:
            # Subtract one to account for the "Create file" item
            directory_index = selected_index - 1

            current_root = self.view.window().folders()[0]

            # The paths are relative to the project root
            file_directory = os.path.join(
                current_root,
                self.step_directories[directory_index])
            view = self.view.window().open_file(file_directory)

        # Append snippet to the view
        sublime.set_timeout(lambda: self._append_snippet(view), 10)

    def _append_snippet(self, view):
        '''
        Append snippet to the chosen file
        '''

        # TODO: This is quite dangerous, maybe we should change this
        if view.is_loading():
            sublime.set_timeout(lambda: self._append_snippet(view), 10)
        else:
            initial_view_size = view.size()
            for step in self.selected_steps:
                snippet = sublime.expand_variables(
                    STEP_SNIPPET,
                    {'type': step.step_type,
                     'name': step.name,
                     'func': step.name.lower().replace('"', '')
                     .replace(' ', '_')})

                view.run_command('append',
                                 {'characters': snippet,
                                  'scroll_to_end': True})

            view.sel().add(sublime.Region(initial_view_size, view.size()))

    def _get_step_directories(self):
        '''
        Get the path of the step files used by behave.
        '''

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
        for selection in self.view.sel():
            current_line_number = self.view.rowcol(selection.begin())[0] + 1

            # Use the location to find the matching step
            # (e.g. features/toolkit.feature:4)
            location = '%s:%d' % (current_file, current_line_number)

            for step in all_steps:
                if step['location'] == location:
                    selected_steps.add(Step(step['step_type'], step['name']))
                    break

        return selected_steps
