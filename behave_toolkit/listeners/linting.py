import sublime_plugin

from ..utils.scope import is_gherkin


class BtHighlightUnimplementedStepsEventListener(sublime_plugin.EventListener):

    """Highlights unimplemented steps."""

    def highlight(self, view):
        if is_gherkin(view):
            view.run_command('bt_highlight_unimplemented_steps')

    def on_activated(self, view):
        self.highlight(view)

    def on_load(self, view):
        self.highlight(view)

    def on_post_save(self, view):
        self.highlight(view)
