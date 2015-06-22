from imp import reload
import sys


reload_mods = []
for mod in sys.modules:
    if mod[0:20] == 'BehaveToolkit' and sys.modules[mod] != None:
        reload_mods.append(mod)

mod_prefix = 'BehaveToolkit.behave_toolkit'

mods_load_order = [
    '',

    '.behave_command',

    '.commands',
    '.commands.generate_missing_step_definitions',
    '.commands.generate_step_definition',
    '.commands.go_to_step_definition',
    '.commands.highlight_undefined_steps',
    '.commands.run_scenario',

    '.listeners',
    '.listeners.linting',

    '.mixins',
    '.mixins.output_panel',
    '.mixins.steps',

    '.utils',
    '.utils.scope'
    '.utils.text'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except (ImportError):
            pass
