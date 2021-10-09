def deprecated_fn(
    from_v,
    to_v,
    alt_fn,
    message="",
):
    """Decorator to mark a function as deprecated.

    Parameters
    ----------
    from_v : str
        Version from since the function is deprecated
    to_v : str
        Version from which the function is removed
    alt_fn: str
        New function to replace the deprecated function
    message : str
        Message to display when the function is called

    Returns
    -------
    function
        The decorated function
    """

    if from_v is None or to_v is None or alt_fn is None:
        raise ValueError("from_v, to_v, and alt_fn cannot be None")

    def decorator(func):
        msg = f"{func.__name__} is deprecated since version {from_v} and will be removed in version {to_v}."
        if alt_fn is not None:
            msg += f" Use {alt_fn} instead."
        
        if message:
            msg = f"{msg} {message}"

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
    message="",
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
    message : str
        Message to display when the function is called

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

        msg = f"{depr_param} is deprecated since version {from_v} and will be removed in version {to_v}."
        if alt_param is not None:
            msg += f" Use {alt_param} instead."
        
        if message:
            msg = f"{msg} {message}"

        def wrapper(*args, **kwargs):
            if depr_param in kwargs:
                deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_default(
    from_v,
    to_v,
    depr_param,
    alt_value=None,
    message="",
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
    message : str
        Message to display when the function is called
        
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
            msg += f" and it will not have a default value in version {to_v}."
        else:
            msg += f" and it will become {depr_param}={alt_value} instead."

        if message:
            msg = f"{msg} {message}"

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
