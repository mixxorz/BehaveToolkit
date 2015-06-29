
def snake_caseify(text):
    """Takes text and returns it in snake case form."""

    return ''.join([e for e in text if e.isalnum() or e == ' ']).replace(
        ' ', '_').lower()
