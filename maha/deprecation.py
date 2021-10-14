__all__ = ["deprecated_fn", "deprecated_param", "deprecated_default"]

from functools import wraps
from typing import Any


def deprecated_fn(from_v: str, to_v: str, alt_fn: str, message: str = ""):
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

        @wraps(func)
        def wrapper(*args, **kwargs):
            deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_param(
    from_v: str,
    to_v: str,
    depr_param: str,
    alt_param: str = None,
    message: str = "",
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

        if alt_param is not None and alt_param not in params:
            raise ValueError(f"{alt_param} is not a parameter of {func.__name__}")

        msg = f"{depr_param} is deprecated since version {from_v} and will be removed in version {to_v}."
        if alt_param is not None:
            msg += f" Use {alt_param} instead."

        if message:
            msg = f"{msg} {message}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            # the first condition checks if it's passed as a keyword argument
            # the second condition checks if it's passed as a positional argument
            # the third condition handles the case where the optional parameter is
            # passed as a positional argument
            positionales = [
                k for k, v in params.items() if v.default is Parameter.empty
            ]
            if (
                depr_param in kwargs
                or depr_param in positionales
                or list(params.keys()).index(depr_param) <= len(args) - 1
            ):
                deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_default(
    from_v: str,
    to_v: str,
    depr_param: str,
    alt_value: Any = None,
    message: str = "",
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

        msg = f"The default value of {depr_param} is deprecated since version {from_v}"
        if alt_value is None:
            msg += f" and will be removed in version {to_v}."
        else:
            msg += f" and will become {depr_param}={alt_value} in version {to_v}."

        if message:
            msg = f"{msg} {message}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            # if the parameter isn't passed as a keyword argument
            if depr_param not in kwargs:
                nonlocal msg
                msg += f" Use {depr_param}={depr_param_default} to preserve the current behavior."

            deprecation_warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecation_warning(msg: str):
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
