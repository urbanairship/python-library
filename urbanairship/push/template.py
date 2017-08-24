def merge_data(template_id, substitutions):
    """Template push merge_data creation.

    :param template_id: Required, UUID.
    :param substitutions: Required, dictionary of template variables and their
        substitutions, e.g. {"FIRST_NAME": "Bob", "LAST_NAME": "Smith"}

    """

    md = {}

    md['template_id'] = template_id
    md['substitutions'] = {
        key: val for key, val in iter(substitutions.items()) if val is not None
    }

    return md