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

    def run(self, edit, **kwargs):

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
        if selected_index == -1:
            return

        # Create new file
        elif selected_index == 0:
            # TODO: Set Syntax of the new file to be python
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
        # TODO: This is quite dangerous, maybe we should change this
        if view.is_loading():
            sublime.set_timeout(lambda: self._append_snippet(view), 10)
        else:
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

    def _get_steps(self, output):
        steps = set()

        Step = namedtuple('Step', ['step_type', 'name', 'keyword', 'location'])

        for feature in output:
            for element in feature['elements']:
                for step in element['steps']:
                    steps.add(Step(step['step_type'],
                                   step['name'],
                                   step['keyword'],
                                   step['location']))

        return steps

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

    def _get_selected_steps(self):
        current_root = self.view.window().folders()[0]
        current_file = self.view.file_name()

        # Convert to relative path
        current_file = os.path.relpath(current_file, current_root)

        json_output = self.behave(current_file, '--dry-run',
                                  '--format', 'json', '--no-summary',
                                  '--no-snippets')

        output = json.loads(json_output)

        steps = self._get_steps(output)

        Step = namedtuple('Step', ['step_type', 'name', 'keyword'])

        selected_steps = set()

        # Find the steps under the cursors
        for selection in self.view.sel():
            current_line_number = self.view.rowcol(selection.begin())[0] + 1

            location = '%s:%d' % (current_file, current_line_number)

            for step in steps:
                if step.location == location:
                    selected_steps.add(Step(step.step_type,
                                            step.name,
                                            step.keyword))
                    break

        return selected_steps
