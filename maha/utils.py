def get_unicode(text: str) -> bytes:
    """Returns the unicode for input text

    Parameters
    ----------
    text : str
        Text to encode

    Returns
    -------
    bytes
        Text with characters encoded in raw unicode.
    """
    return text.encode("raw_unicode_escape")


def check_positive_integer(value: float, var_name: str):
    """Raises ValueError if the input value is not a positive integer.

    Parameters
    ----------
    value : float
        Input value
    var_name : str
        Variable name to include it in the error message

    Raises
    ------
    ValueError
        if the input value is not a positive integer.
    """
    if value < 1:
        raise ValueError(f"'{var_name}' should be greater than 0")

    if value != int(value):
        raise ValueError(f"Cannot assign a float value to '{var_name}'")


def deprecated_fn(
    from_v,
    to_v,
    alt_fn=None,
):
    """Decorator to mark a function as deprecated.

    Parameters
    ----------
    from_v : str
        Version from since the function is deprecated
    to_v : str
        Version from which the function is removed
    message : str
        Message to display when the function is called

    Returns
    -------
    function
        The decorated function
    """

    if from_v is None or to_v is None:
        raise ValueError("from_v and to_v cannot be None")

    def decorator(func):
        msg = f"{func.__name__} is deprecated since version {from_v} and will be removed on version {to_v}."
        if alt_fn is not None:
            msg += f" Use {alt_fn} instead."

        def wrapper(*args, **kwargs):
            deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_param(
    from_v,
    to_v,
    depr_param,
    alt_param,
):
    """Decorator to mark a parameter as deprecated.

    Parameters
    ----------
    from_v : str
        Version since which the parameter is deprecated
    to_v : str
        Version from which the parameter is removed
    depr_param: str
        Parameter to deprecate
    alt_param: str
        Parameter to use instead

    Returns
    -------
    function
        The decorated function
    """

    if from_v is None or to_v is None or depr_param is None:
        raise ValueError("from_v, to_v and depr_param cannot be None")

    def decorator(func):
        from inspect import Parameter, signature

        sig = signature(func)
        params = sig.parameters

        if depr_param not in params:
            raise ValueError(f"{depr_param} is not a parameter of {func.__name__}")

        msg = f"{depr_param} is deprecated since version {from_v} and will be removed on version {to_v}."
        if alt_param is not None:
            msg += f" Use {alt_param} instead."

        def wrapper(*args, **kwargs):
            deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_default(
    from_v,
    to_v,
    depr_param,
    alt_value=None,
):
    """Decorator to mark a parameter default value as deprecated.

    Parameters
    ----------
    from_v : str
        Version since which the parameter is deprecated
    to_v : str
        Version from which the parameter is removed
    depr_param: str
        Parameter to deprecate its default value
    alt_value: str
        New default value that will used instead

    Returns
    -------
    function
        The decorated function
    """

    if from_v is None or to_v is None or depr_param is None:
        raise ValueError("from_v, to_v and depr_param cannot be None")

    def decorator(func):
        from inspect import Parameter, signature

        sig = signature(func)
        params = sig.parameters

        if depr_param not in params:
            raise ValueError(f"{depr_param} is not a parameter of {func.__name__}")

        if params[depr_param].default is Parameter.empty:
            raise ValueError(f"{depr_param} has no default value")

        depr_param_default = params[depr_param].default

        msg = f"{depr_param}={depr_param_default} is deprecated since version {from_v}"
        if alt_value is None:
            msg += f" and it will not have a default value on version {to_v}."
        else:
            msg += f" and it will become {depr_param}={alt_value} instead."

        def wrapper(*args, **kwargs):
            deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecation_warning(msg):
    """Prints a deprecation warning.

    Parameters
    ----------
    msg : str
        Message to print
    """
    import warnings

    warnings.warn(
        msg,
        DeprecationWarning,
        stacklevel=2,
    )
