import imp
import sys

if sys.version_info < (3, 3):
    raise RuntimeError('BehaveSublimeToolkit does not support Sublime Text 2.')


# Reloader
reloader_name = 'BehaveSublimeToolkit.behave_sublime_toolkit.reloader'
if reloader_name in sys.modules:
    imp.reload(sys.modules[reloader_name])

from .behave_sublime_toolkit.reloader import *
from .behave_sublime_toolkit.commands import *
