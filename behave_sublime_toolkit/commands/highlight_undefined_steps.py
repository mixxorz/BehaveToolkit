from collections import namedtuple
import re

import sublime
import sublime_plugin

from ..behave_command import BehaveCommand


class BstHighlightUndefinedSteps(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Highlights undefined steps in a feature file.

    This command uses the 'steps.usage' format and parses its output to
    get the undefined steps.
    '''

    def run(self, edit, **kwargs):
        sublime.set_timeout_async(self.run_async, 0)

    def run_async(self):

        output = self.behave('--dry-run',
                             '--format',
                             'steps.usage',
                             '--no-summary',
                             '--no-snippets')
        offset = output.find('UNDEFINED STEPS')

        region_name = 'bst.undefined_steps'

        if offset != -1:
            output = output[offset:]

            # TODO: Improve this regex for better step name matching
            p = re.compile('^\s\s([\w+\s"]+)\s*#\s(.*):(\d+)$', re.MULTILINE)

            matched_set = re.findall(p, output)
            undefined_steps = []

            Step = namedtuple('Step', ['name', 'file', 'line', 'region'])

            for match in matched_set:
                name = match[0].strip()
                step = Step(name, match[1], match[2], self.view.find(name, 0))

                undefined_steps.append(step)

            self.view.add_regions(region_name,
                                  [step.region for step in undefined_steps],
                                  'comment')
        else:
            # Clear regions if we can't find UNDEFINED STEPS in the output
            self.view.erase_regions(region_name)
