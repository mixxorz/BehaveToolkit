from ..utils import parser


class StepsMixin(object):

    """Provies methods for dealing with steps."""

    def get_used_steps(self, project_wide=False):
        """Returns a list of Steps that are being used.

        It only returns steps related to the current active file.

        Arguments:
            project_wide -- If True, will return project wide step data.

        """

        step_data = self._get_step_data()

        used_steps = parser.parse_used_steps(step_data)

        return used_steps

    def get_unused_steps(self, project_wide=False):
        """Returns a list of Steps that are unused.

        It only returns steps related to the current active file.

        Arguments:
            project_wide -- If True, will return project wide step data.

        """

        step_data = self._get_step_data(project_wide=project_wide)

        unused_steps = parser.parse_unused_steps(step_data)

        return unused_steps

    def get_unimplemented_steps(self, project_wide=False):
        """Returns a list of Usages that are unimplemented.

        It only returns steps related to the current active file.

        Arguments:
            project_wide -- If True, will return project wide step data.

        """

        step_data = self._get_step_data()

        undefined_steps = parser.parse_unimplemented_steps(step_data)

        return undefined_steps

    def _get_step_data(self, project_wide=False):
        """Calls behave and returns its output.

        Calls behave with both the json formatter and the steps.usage
        formatter. Suprisingly, it returns both formats.

        It only returns steps related to the current active file.

        Arguments:
            project_wide -- If True, will return project wide step data.

        Returns: step_data (str)
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

        step_data = self.behave(*args)

        return step_data
