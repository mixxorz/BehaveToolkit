PANEL_NAME = 'bt_behave_output'


class OutputPanelMixin(object):

    """Provides methods for working with output panels."""

    def _get_output_view(self, panel_name):
        """Returns the output panel specified by panel_name.

        The method also creates the output panel if it doesn't exist.

        Arguments:
            panel_name -- the name of the output panel

        """

        if not hasattr(self, 'output_view'):
            self.output_view = self.view.window().get_output_panel(panel_name)
        return self.output_view

    def append(self, text, panel_name=PANEL_NAME, end='\n'):
        """Appends a line to output panel panel_name.

        The method also creates the output panel if output panel panel_name
        doesn't exist.

        Arguments:
            panel_name -- the name of the output panel
        """
        output_view = self._get_output_view(panel_name)

        # TODO: Style the output
        output_view.run_command('append', {'characters': text + end,
                                           'scroll_to_end': True})
        self.view.window().run_command('show_panel',
                                       {'panel': 'output.%s' % panel_name})

    def erase(self, panel_name=PANEL_NAME):
        """Clears the output panel.

        Arguments:
            panel_name -- the name of the output panel
        """
        output_view = self._get_output_view(panel_name)

        output_view.run_command("select_all")
        output_view.run_command("right_delete")
