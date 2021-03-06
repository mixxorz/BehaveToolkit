from behave import given, when, then


@given(u'a thing')
def a_thing(context):
    pass


@when(u'a something happens')
def something_happens(context):
    pass


@then(u'a thing should happen')
def thing_should_happen(context):
    pass


@given(u'a second thing')
def second_thing(context):
    pass


@when(u'a second thing happens')
def second_thing_happens(context):
    pass


@then(u'a second thing should happen')
def second_thing_should_happen(context):
    pass


@given(u'a third thing')
def a_third_thing(context):
    raise NotImplementedError(u'STEP: a third thing')



@then(u'it will fail')
def it_will_fail(context):
    raise NotImplementedError(u'STEP: it will fail')

