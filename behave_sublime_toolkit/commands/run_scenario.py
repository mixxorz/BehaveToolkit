import sublime
import sublime_plugin


class BstRunScenario(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        current_line_number = self.view.rowcol(
            self.view.sel()[0].begin())[0] + 1
        sublime.status_message('Line number: %d' % current_line_number)
        # sublime.message_dialog(os.getenv('VIRTUAL_ENV', 'None'))
        python = self.view.settings().get('python_interpreter', 'python')

        sublime.active_window().active_view().run_command(
            'bst_display_panel', {'msg': python})
