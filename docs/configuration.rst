Configuration
=============


behave_command
--------------

The command used to run behave.

By default, ``BehaveToolkit`` tries to find ``behave`` in your environment.
Change this setting if you want to specifically set how ``behave`` gets
executed.

Open ``Preferences > Package Settings > BehaveToolkit > Settings - User`` and
paste the following (for example):

.. code-block:: json

  {
    "behave_command": ["/Users/mixxorz/.virtualenvs/myproject/bin/behave"]
  }


You can override the setting in your the sublime-project file of your
project too. This will take priority over the global settings.

*myproject.sublime-project*

.. code-block:: json

  {
    "folders":
    [
      {
        "path": "/Users/mixxorz/Projects/myproject"
      }
    ],
    "settings":
    {
      "behave_command": ["/Users/mixxorz/.virtualenvs/myproject/bin/behave"]
    }
  }


If you're using `behave-django`_, another project by me which integrates
``behave`` and ``Django``, you can configure ``behave_command`` like this.

.. code-block:: json

  {
    "behave_command": [
      "/Users/mixxorz/.virtualenvs/myproject/bin/python",
      "/Users/mixxorz/Projects/myproject/manage.py",
      "behave"
    ]
  }


.. _behave-django: https://github.com/mixxorz/behave-django
