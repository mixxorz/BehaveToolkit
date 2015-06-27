from collections import namedtuple
import json
import re

Step = namedtuple('Step', ['func', 'path', 'line', 'usages'])
Usage = namedtuple('Usage', ['name', 'path', 'line', 'type', 'keyword'])


def parse_used_steps(step_data):
    """
    Returns a list of Steps that are being used.

    Keyword arguments:
        step_data -- str returned by `_get_step_data()`

    """

    steps_output, json_output = parse_sections(step_data)

    json_data = json.loads(json_output)

    # All steps from  json data
    # Key is the step location, value is the step type.
    step_type_dict = {}

    for feature in json_data:
        for element in feature['elements']:
            for step in element['steps']:
                step_type_dict[step['location']] = step

    section_pattern = re.compile('(^@.*?)(UN|$)', re.DOTALL)
    section = re.search(section_pattern, steps_output)

    if section is None:
        return []

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

            parsed_usages.append(
                Usage(step_type_dict[location]['name'],
                      usage[1].strip(),
                      int(usage[2].strip()),
                      step_type_dict[location]['step_type'],
                      step_type_dict[location]['keyword']))

        parsed_steps.append(Step(func.group(1).strip(),
                                 func.group(2).strip(),
                                 int(func.group(3).strip()),
                                 parsed_usages))

    return parsed_steps


def parse_unused_steps(step_data):
    """
    Returns a list of Steps that are unused.

    Keyword arguments:
        step_data -- str returned by `_get_step_data()`

    """

    steps_output, json_output = parse_sections(step_data)

    unused_step_pattern = re.compile('^ {2}(@.*)#(.*):(\d+)', re.MULTILINE)

    parsed_steps = []

    for step in re.finditer(unused_step_pattern, steps_output):
        parsed_steps.append(Step(step.group(1).strip(),
                                 step.group(2).strip(),
                                 int(step.group(3).strip()),
                                 []))

    return parsed_steps


def parse_undefined_steps(step_data):
    """
    Returns a list of Usages that are undefined.

    Keyword arguments:
        step_data -- str returned by `_get_step_data()`

    """

    steps_output, json_output = parse_sections(step_data)

    json_data = json.loads(json_output)

    # All steps from  json data
    # Key is the step location, value is the step type.
    step_type_dict = {}

    for feature in json_data:
        for element in feature['elements']:
            for step in element['steps']:
                step_type_dict[step['location']] = step

    section_pattern = re.compile('UNDEFINED STEPS\[\d+\]:(.*)',
                                 re.DOTALL)

    section_match = re.search(section_pattern, steps_output)

    parsed_steps = []

    if section_match:
        section = section_match.group(1)

        single_step_pattern = re.compile('(.*)#(.*):(\d+)', re.MULTILINE)

        for step in re.finditer(single_step_pattern, section):

            location = '%s:%s' % (step.group(2).strip(),
                                  step.group(3).strip())

            parsed_steps.append(
                Usage(step_type_dict[location]['name'],
                      step.group(2).strip(),
                      int(step.group(3).strip()),
                      step_type_dict[location]['step_type'],
                      step_type_dict[location]['keyword']))

    return parsed_steps


def parse_sections(step_data):
    """
    Parse out the json and steps information from step_data

    Returns: steps_output, json_output
    """
    json_pattern = re.compile('(.*\])\n', re.DOTALL)
    json_match = re.search(json_pattern, step_data)
    json_output = json_match.group(1)

    steps_output = step_data[json_match.end(0):]

    return steps_output, json_output
