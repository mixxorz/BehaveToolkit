from collections import namedtuple
import json
import re

Step = namedtuple('Step', ['func', 'path', 'line', 'usages'])
Usage = namedtuple('Usage', ['name', 'path', 'line', 'type'])


class StepsMixin(object):

    '''
    Provies methods for dealing with steps
    '''

    def get_used_steps(self, project_wide=False):
        """
        Returns a list of Steps that are being used.

        It only returns steps related to the current active file.

        Keyword arguments:
            project_wide -- If True, will return project wide step data.

        """

        json_output, output = self._get_output(project_wide=project_wide)

        json_data = json.loads(json_output)

        # All steps from  json data
        # Key is the step location, value is the step type.
        step_type_dict = {}

        for feature in json_data:
            for element in feature['elements']:
                for step in element['steps']:
                    step_type_dict[step['location']] = step['step_type']

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

                location = '%s:%s' % (usage[1].strip(),
                                      usage[2].strip())

                parsed_usages.append(Usage(usage[0].strip(),
                                           usage[1].strip(),
                                           int(usage[2].strip()),
                                           step_type_dict[location]))

            parsed_steps.append(Step(func.group(1).strip(),
                                     func.group(2).strip(),
                                     int(func.group(3).strip()),
                                     parsed_usages))

        return parsed_steps

    def get_unused_steps(self, project_wide=False):
        """
        Returns a list of Steps that are unused.

        It only returns steps related to the current active file.

        Keyword arguments:
            project_wide -- If True, will return project wide step data.

        """

        json_output, output = self._get_output(project_wide=project_wide)

        unused_step_pattern = re.compile('^ {2}(@.*)#(.*):(\d+)', re.MULTILINE)

        parsed_steps = []

        for step in re.finditer(unused_step_pattern, output):
            parsed_steps.append(Step(step.group(1).strip(),
                                     step.group(2).strip(),
                                     int(step.group(3).strip()),
                                     []))

        return parsed_steps

    def get_undefined_steps(self, project_wide=False):
        """
        Returns a list of Usages that are undefined.

        It only returns steps related to the current active file.

        Keyword arguments:
            project_wide -- If True, will return project wide step data.

        """

        json_output, output = self._get_output(project_wide=project_wide)

        json_data = json.loads(json_output)

        # All steps from  json data
        # Key is the step location, value is the step type.
        step_type_dict = {}

        for feature in json_data:
            for element in feature['elements']:
                for step in element['steps']:
                    step_type_dict[step['location']] = step['step_type']

        section_pattern = re.compile('UNDEFINED STEPS\[[\d+]\]:(.*)',
                                     re.DOTALL)

        section_match = re.search(section_pattern, output)

        parsed_steps = []

        if section_match:
            section = section_match.group(1)

            single_step_pattern = re.compile('(.*)#(.*):(\d+)', re.MULTILINE)

            for step in re.finditer(single_step_pattern, section):

                location = '%s:%s' % (step.group(2).strip(),
                                      step.group(3).strip())

                parsed_steps.append(Usage(step.group(1).strip(),
                                          step.group(2).strip(),
                                          int(step.group(3).strip()),
                                          step_type_dict[location]))

        return parsed_steps

    def _get_output(self, project_wide):
        """
        Returns the json and step output by calling `behave`.

        Calls behave with both the json formatter and the steps.usage
        formatter. Suprisingly, it returns both formats.

        It only returns steps related to the current active file.

        Keyword arguments:
            project_wide -- If True, will return project wide step data.

        Returns (json_output, steps_output) ; both str
        """

        args = ['--dry-run',
                '--format',
                'json',
                '--format',
                'steps.usage',
                '--no-summary',
                '--no-snippets'
                ]

        if not project_wide:
            args.append(self.view.file_name())

        output = self.behave(*args)

        json_pattern = re.compile('(.*\])\n', re.DOTALL)
        json_match = re.search(json_pattern, output)
        json_output = json_match.group(1)

        steps_output = output[json_match.end(0):]

        return json_output, steps_output
