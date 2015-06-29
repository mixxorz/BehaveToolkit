Getting Started
===============

Setup
-----

Make sure you have ``behave`` and ``BehaveToolkit`` `installed`_.

Then, let's start create our project structure

.. code::

  myproject/
    features/
      steps/
      myfeature.feature

Let's open the project directory in sublime:

.. code::

  $ subl myproject/

Let's add a sample scenario:

.. code::

  # myproject/features/myfeature.feature
  Feature: My feature

    Scenario: Addition between two numbers
      Given the first number is "1"
        And the second number is "1"
       When I add them together
       Then I should get "2"


Once you hit save, you should see undefined steps get highlighted.

Generate Step Definition
------------------------

Let's try to generate some step definitions. Place the cursor over an undefined
step, open up the command palette and select
``Behave: Generate Step Definition``.

screenshot should be here

You should be prompted to create a new file. Let's do that.

screenshot should be here

Let's save this file under ``myproject/features/steps/steps.py``

Once it's saved, when you go back to ``myfeature.feature``, you should see the
step be cleared.

screenshot here

Generate Missing Step Definitions
---------------------------------

Let's generate the rest of the steps. With the feature file in focus, let's
open up the command palette and select
``Behave: Generate Missing Step Definitions``.

screenshot here

You're now given a choice of either creating a new file, or an existing step
file. Let's choose ``steps.py``.

screenshot here

You should now see the generate step definitions pasted inside ``steps.py``.

screenshot here

Once you hit save and go back to the feature file, you should see that all
steps are now cleared.

Running the scenario
--------------------

In lieu with the spirit of TDD, let's watch the tests fail.

Place the cursor on a scenario, open the command palette and select
``Behave: Run Scenario``. You should see the test failing.

.. code::

  Feature: My feature # features/myfeature.feature:1

    Scenario: Addition between two numbers  # features/myfeature.feature:3
      Given the first number is "1"         # features/steps/steps.py:14
        Traceback (most recent call last):
          File "/Users/mixxorz/.pyenv/versions/2.7.10/lib/python2.7/site-packages/behave/model.py", line 1456, in run
            match.run(runner.context)
          File "/Users/mixxorz/.pyenv/versions/2.7.10/lib/python2.7/site-packages/behave/model.py", line 1903, in run
            self.func(context, *args, **kwargs)
          File "features/steps/steps.py", line 16, in the_first_number_is_1
            raise NotImplementedError(u'STEP: the first number is "1"')
        NotImplementedError: STEP: the first number is "1"

      And the second number is "1"          # None
      When I add them together              # None
      Then I should get "2"                 # None


  Failing scenarios:
    features/myfeature.feature:3  Addition between two numbers

  0 features passed, 1 failed, 0 skipped
  0 scenarios passed, 1 failed, 0 skipped
  0 steps passed, 1 failed, 3 skipped, 0 undefined
  Took 0m0.000s

Let's implement the tests.

.. code:: python

  # myproject/features/steps/steps.py
  from behave import given, when, then


  @when(u'I add them together')
  def i_add_them_together(context):
      context._sum = context._first_num + context._second_num


  @then(u'I should get "{num:d}"')
  def i_should_get_2(context, num):
      assert num == context._sum


  @given(u'the first number is "{num:d}"')
  def the_first_number_is_1(context, num):
      context._first_num = num


  @given(u'the second number is "{num:d}"')
  def the_second_number_is_1(context, num):
      context._second_num = num

When you run the scenario, the tests should now pass:

.. code::

  Feature: My feature # features/myfeature.feature:1

    Scenario: Addition between two numbers  # features/myfeature.feature:3
      Given the first number is "1"         # features/steps/steps.py:14
      And the second number is "1"          # features/steps/steps.py:19
      When I add them together              # features/steps/steps.py:4
      Then I should get "2"                 # features/steps/steps.py:9

  1 feature passed, 0 failed, 0 skipped
  1 scenario passed, 0 failed, 0 skipped
  4 steps passed, 0 failed, 0 skipped, 0 undefined
  Took 0m0.001s

Specific Scenarios
~~~~~~~~~~~~~~~~~~

If you want, you can run only specific scenarios. Let's add a new scenario,
with different numbers this time.

.. code:: gherkin

  Scenario: Addition between different numbers
    Given the first number is "2"
      And the second number is "3"
     When I add them together
     Then I should get "5"

Place the cursor over the second scenario. When you run the scenario, it will
only run the scenario under your cursor.

Running All Scenarios In The Current Feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to run all scenarios in the current feature, just place your cursor
on the first line of the feature file, and run the scenario

Running Everything
~~~~~~~~~~~~~~~~~~

If you want to run all scenarios in all features, just run the scenario while
you don't have a feature file open.


.. _installed: /installation.html
