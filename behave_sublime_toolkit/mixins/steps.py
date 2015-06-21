from collections import namedtuple
import re


class StepsMixin(object):

    '''
    Provies methods for dealing with steps
    '''

    def get_undefined_steps(self):
        '''
        Gets undefined steps for the current view as a list of namedtuples.
        The namedtuple is defined as:

        `Step = namedtuple('Step', ['name', 'path', 'line'])`

        name - The name of the step
        path - Path of the feature file the step belongs to
        line - Its line number in the feature file
        '''

        output = self.behave('--dry-run',
                             '--format',
                             'steps.usage',
                             '--no-summary',
                             '--no-snippets')
        offset = output.find('UNDEFINED STEPS')

        if offset != -1:
            output = output[offset:]

            p = re.compile('^(.+)\s*#\s(.*):(\d+)$', re.MULTILINE)

            matched_set = re.findall(p, output)
            undefined_steps = []

            Step = namedtuple('Step', ['name', 'path', 'line'])

            for match in matched_set:
                step = Step(match[0].strip(), match[1], match[2])

                undefined_steps.append(step)

            return undefined_steps
        else:
            return []
