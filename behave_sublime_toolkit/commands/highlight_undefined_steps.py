from collections import namedtuple
import re

import sublime_plugin

from ..behave_command import BehaveCommand


class BstHighlightUndefinedSteps(sublime_plugin.TextCommand, BehaveCommand):

    '''
    Highlights undefined steps in a feature file
    '''

    def run(self, edit, **kwargs):

        output = self.behave('--dry-run',
                             '--format',
                             'steps.usage',
                             '--no-summary',
                             '--no-snippets')
        offset = output.find('UNDEFINED STEPS')

        if offset != -1:
            output = output[offset:]

            p = re.compile('^\s\s([\w+\s"]+)\s*#\s(.*):(\d+)$', re.MULTILINE)

            matched_set = re.findall(p, output)
            undefined_steps = []

            Step = namedtuple('Step', ['name', 'file', 'line', 'region'])

            for match in matched_set:
                name = match[0].strip()
                step = Step(name, match[1], match[2], self.view.find(name, 0))

                undefined_steps.append(step)

            self.view.add_regions('undefined_steps',
                                  [step.region for step in undefined_steps],
                                  'comment')
