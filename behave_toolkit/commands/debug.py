"""Commands used for debugging purposes."""

import imp
import sys

import sublime
import sublime_plugin


class BtReloadModules(sublime_plugin.WindowCommand):

    """Reloads all BehaveToolkit modules."""

    def run(self):
        modules = [module for module in sys.modules.keys()
                   if module[:13] == 'BehaveToolkit']
        for _ in range(2):
            for name in modules:
                print('[BehaveToolkit] Reloading submodule: ', name)
                imp.reload(sys.modules[name])

        sublime.sublime_api.plugin_host_ready()

    def is_visible(self):
        """This command is only visible during debug mode"""
        settings = sublime.load_settings('BehaveToolkit.sublime-settings')
        return settings.get('debug')
