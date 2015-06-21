from imp import reload
import sys


reload_mods = []
for mod in sys.modules:
    if mod[0:20] == 'BehaveSublimeToolkit' and sys.modules[mod] != None:
        reload_mods.append(mod)

mod_prefix = 'BehaveSublimeToolkit.behave_sublime_toolkit'

mods_load_order = [
    '',

    '.behave_command',

    '.commands',
    '.commands.highlight_undefined_steps',
    '.commands.run_scenario',

    '.listeners',
    '.listeners.linting',

    '.utils',
    '.utils.log'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except (ImportError):
            pass
