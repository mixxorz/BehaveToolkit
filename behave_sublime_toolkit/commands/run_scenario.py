import json
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstRunScenario(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Runs the behave scenario under the cursor

    How it behaves:

        - If the cursor is located before any scenario, run the feature.
        - If the cursor is below a scenario, run that scenario only.
        - If there are multiple cursors, all of them will be run based on
          the rules set forth above.
    '''

    def run(self, edit, **kwargs):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):
        self.behave('--no-skipped', *self._get_tests_part(), output=True)

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

        # Gets JSON information about the current feature file
        # via the 'json' behave formatter

        json_output = self.behave(current_file, '--dry-run',
                                  '--format', 'json', '--no-summary',
                                  '--no-snippets')

        output = json.loads(json_output)

        # The location of the first scenario (e.g. features/toolkit.feature:4)
        first_scenario_location = output[0][
            'elements'][0]['steps'][0]['location']

        # Extract the line number of the first scenario
        m = re.search(':(\d+)', first_scenario_location)
        line_number = int(m.group(1))
        # The line number returned is aligned to the first step. So we subtract
        # 1
        line_number -= 1

        for selection in self.view.sel():
            current_line_number = self.view.rowcol(selection.begin())[0] + 1

            # If the cursor is below the first scenario, run a scenario
            if current_line_number >= line_number:
                tests.append('%s:%s' % (current_file, current_line_number))

            # If the cursor is above, run the feature
            else:
                if current_file not in tests:
                    tests.append(current_file)

        return tests
