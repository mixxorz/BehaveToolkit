import json
import os
import re
import subprocess

import sublime_plugin

from ..utils.log import OutputPanelMixin


class BstRunScenario(sublime_plugin.TextCommand, OutputPanelMixin):

    '''
    Runs the behave scenario under the cursor

    How it behaves:

        - If the cursor is located before any scenario, run the feature.
        - If the cursor is below a scenario, run that scenario only.
        - If there are multiple cursors, all of them will be run based on
          the rules set forth above.
    '''

    def run(self, edit, **kwargs):
        args = []

        self.python = self.view.settings().get('python_interpreter', 'python')
        self.behave = os.path.join(os.path.dirname(self.python), 'behave')

        args = [self.python,
                self.behave,
                '--no-skipped',
                ] + self._get_tests_part()

        with subprocess.Popen(args,
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              cwd=self.view.window().folders()[0]) as p:

            self.erase()
            for line in p.stdout:
                self.append(line, end='')

    def _get_tests_part(self):
        '''
        Returns positional arguments for behave to specify which
        features/scenarios to run
        '''

        # If we're not looking at a Gherkin file, just run everything
        if 'gherkin' not in self.view.scope_name(0):
            return []

        # Scenario locations are stored here
        # e.g. ['features/toolkit.feature:4', 'features/toolkit.feature:8']
        tests = []
        current_file = self.view.file_name()

        # TODO: Extract this to a behave API wrapper
        # Gets JSON information about the current feature file
        # via the 'json' behave formatter
        args = [self.python, self.behave, current_file, '-d',
                '-f', 'json', '--no-summary', '--no-snippets']

        json_output = ''

        with subprocess.Popen(args,
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              cwd=self.view.window().folders()[0]) as p:

            for line in p.stdout:
                json_output += line

        output = json.loads(json_output)

        # The location of the first scenario (e.g. features/toolkit.feature:4)
        first_scenario_location = output[0][
            'elements'][0]['steps'][0]['location']

        # Extract the line number of the first scenario
        m = re.search(':(\d+)', first_scenario_location)
        line_number = int(m.group(1))

        for selection in self.view.sel():
            current_line_number = self.view.rowcol(selection.begin())[0] + 1

            # If the cursor is below the first scenario, run a scenario
            if current_line_number > line_number:
                tests.append('%s:%s' % (current_file, current_line_number))

            # If the cursor is above, run the feature
            else:
                if current_file not in tests:
                    tests.append(current_file)

        return tests
