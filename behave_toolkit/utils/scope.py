
def is_python(view):
    """Determine if the given view location is python code."""

    return _is_in_scope(view, matcher='source.python - string - comment')


def is_gherkin(view):
    """Determine if the given view location is a feature file."""

    return _is_in_scope(view, matcher='text.gherkin.feature')


def _is_in_scope(view, matcher=None):
    if view is None:
        return False

    try:
        location = view.sel()[0].begin()
    except IndexError:
        return False

    return view.match_selector(location, matcher)
