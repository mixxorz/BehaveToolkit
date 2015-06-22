import imp
import sys

if sys.version_info < (3, 3):
    raise RuntimeError('BehaveToolkit does not support Sublime Text 2.')


# Reloader
reloader_name = 'BehaveToolkit.behave_toolkit.reloader'
if reloader_name in sys.modules:
    imp.reload(sys.modules[reloader_name])

from .behave_toolkit.reloader import *
from .behave_toolkit.commands import *
from .behave_toolkit.listeners import *
