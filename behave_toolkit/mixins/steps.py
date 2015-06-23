from collections import namedtuple
import re

Step = namedtuple('Step', ['func', 'path', 'line', 'usages'])
Usage = namedtuple('Usage', ['name', 'path', 'line'])


class StepsMixin(object):

    '''
    Provies methods for dealing with steps
    '''

    def get_used_steps(self):
        """Returns a list of Steps that are being used."""

        output = self._get_output()

        section_pattern = re.compile('(^@.*?)(UN|$)', re.DOTALL)
        section = re.search(section_pattern, output)

        step_pattern = re.compile('(.*?)\n\n', re.DOTALL)
        steps = re.findall(step_pattern, section.group(1))

        func_pattern = re.compile('^(@.*)#(.*):(\d+)', re.MULTILINE)
        usage_pattern = re.compile('^\s+(.*)#(.*):(\d+)', re.MULTILINE)

        parsed_steps = []

        for step in steps:
            func = re.search(func_pattern, step)

            usages = re.findall(usage_pattern, step)

            parsed_usages = []

            for usage in usages:
                parsed_usages.append(Usage(usage[0].strip(),
                                           usage[1].strip(),
                                           int(usage[2].strip())))

            parsed_steps.append(Step(func.group(1).strip(),
                                     func.group(2).strip(),
                                     int(func.group(3).strip()),
                                     parsed_usages))

        return parsed_steps

    def get_unused_steps(self):
        """Returns a list of Steps that are unused."""

        output = self._get_output()

        unused_step_pattern = re.compile('^ {2}(@.*)#(.*):(\d+)', re.MULTILINE)

        parsed_steps = []

        for step in re.finditer(unused_step_pattern, output):
            parsed_steps.append(Step(step.group(1).strip(),
                                     step.group(2).strip(),
                                     int(step.group(3).strip()),
                                     []))

        return parsed_steps

    def get_undefined_steps(self):
        """Returns a list of Usages that are undefined."""

        output = self._get_output()

        section_pattern = re.compile('UNDEFINED STEPS\[[\d+]\]:(.*)',
                                     re.DOTALL)

        section_match = re.search(section_pattern, output)

        parsed_steps = []

        if section_match:
            section = section_match.group(1)

            single_step_pattern = re.compile('(.*)#(.*):(\d+)', re.MULTILINE)

            for step in re.finditer(single_step_pattern, section):
                parsed_steps.append(Usage(step.group(1).strip(),
                                          step.group(2).strip(),
                                          int(step.group(3).strip())))

        return parsed_steps

    def _get_output(self):
        """Calls `behave` to get steps data."""

        output = self.behave(self.view.file_name(),
                             '--dry-run',
                             '--format',
                             'steps.usage',
                             '--no-summary',
                             '--no-snippets')

        return output
