PANEL_NAME = 'BehaveSublimeToolkit'


class OutputPanelMixin(object):

    def append(self, edit, text, panel_name=PANEL_NAME, end='\n'):
        if not hasattr(self, 'output_view'):
            self.output_view = self.view.window().get_output_panel(panel_name)
        output_view = self.output_view

        # TODO: Style the output
        output_view.run_command('append', {'characters': text + end,
                                           'scroll_to_end': True})
        self.view.window().run_command('show_panel',
                                       {'panel': 'output.%s' % panel_name})
