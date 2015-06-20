PANEL_NAME = 'BehaveSublimeToolkit'


class OutputPanelMixin(object):

    def append(self, edit, text, panel_name=PANEL_NAME):
        if not hasattr(self, 'output_view'):
            self.output_view = self.view.window().get_output_panel(panel_name)
        output_view = self.output_view

        output_view.insert(edit, output_view.size(), text + '\n')
        output_view.show(output_view.size())
        self.view.window().run_command(
            'show_panel', {'panel': 'output.{}'.format(panel_name)})
