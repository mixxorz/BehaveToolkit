
def snake_caseify(text):
    ''.join([e for e in text if e.isalnum() or e == ' ']).replace(
        ' ', '_').lower()
