Commands
========

Generate Step Function
----------------------------

Generates step functions for steps under the cursor(s).

- Default Keybinding: ``None``

- Command: ``bt_generate_step_function``

Gives you the ability to quickly generate functions for steps. Place the
cursor under a step (e.g. ``Given the first number is "1"``), open the command
palette and select ``Behave: Generate Step Function``. You will be
prompted whether you want to create a new file for this step function, or
to paste it to an existing steps file.

You can also generate multiple step functions at once by placing cursors
on multiple steps.

Generate Missing Step Functions
-------------------------------------

Generates step functions for missing steps.

- Default Keybinding: ``None``

- Command: ``bt_generate_missing_step_functions``

This command is just a convenience command to generate step functions for
all unimplemented steps in the open feature file.

Go To Step Function
-------------------------

Navigate to the step function of the step under the cursor.

- Default Keybinding: ``None``

- Command: ``bt_go_to_step_function``

Does what it says on the tin.

Run behave
----------

Runs behave within the current context.

- Default Keybinding: ``None``

- Command: ``bt_run_behave``

This command is activated by selecting ``Behave: Run behave`` on the command
palette.

- If the cursor is within a Scenario definition, the command will only run that
  scenario.

- If the cursor is above the first Scenario, the command will run all Scenarios
  in that Feature.

- If a feature file isn't visible, the command will run all Scenarios in all
  Features

- If there are multiple cursors, the command will run all Scenarios that are
  under the cursors.
