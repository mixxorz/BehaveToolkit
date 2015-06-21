import sublime_plugin


class BstHighlightUndefinedStepsEventListener(sublime_plugin.EventListener):

    def highlight(self, view):
        if 'gherkin' in view.scope_name(0):
            view.run_command('bst_highlight_undefined_steps')

    def on_load(self, view):
        self.highlight(view)

    def on_post_save(self, view):
        self.highlight(view)
