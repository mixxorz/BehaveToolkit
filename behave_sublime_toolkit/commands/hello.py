import sublime
import sublime_plugin


class BstHello(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.message_dialog('Hello, Amanda!')
