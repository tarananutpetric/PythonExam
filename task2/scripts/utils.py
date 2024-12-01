def CheckAllowedOptions(variable, allowed_options):
    """
    Auxiliary function to check whether a variable is in a list of allowed variables or a list of variables is a subset of the list  of allowed variables.
    :param variable: variable or list of variables  to be checked
    :param allowed_options: list of allowed options for this variable
    """
    if isinstance(variable, list):
        if set(variable).issubset(allowed_options):
            return
    if variable in allowed_options:
        return
    raise ValueError(
        f"Option: {variable} unsupported or not compatible with other selected parameters. Please choose among available options: {allowed_options}."
    )
