import pytest

from maha.deprecation import deprecated_default, deprecated_fn, deprecated_param


def _get_warning_msg(recwarn):
    w = recwarn.pop(DeprecationWarning)
    return w.message.args[0]


def test_deprecated_default(recwarn):
    @deprecated_default(from_v="0.2.0", to_v="0.5.0", depr_param="arg11")
    def f(arg11=1):
        pass

    f()
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg
    assert "arg11=1" in msg


def test_deprecated_default_with_alt(recwarn):
    @deprecated_default(from_v="0.2.0", to_v="0.5.0", depr_param="arg11", alt_value=999)
    def f(arg11=1):
        pass

    f()
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg
    assert "999" in msg
    assert "arg11=1" in msg


def test_deprecated_default_with_passed_argument(recwarn):
    @deprecated_default(
        from_v="0.2.0", to_v="0.5.0", depr_param="arg11", alt_value="None"
    )
    def f(arg11=1):
        pass

    f(arg11=3)
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg
    assert "None" in msg
    assert "arg11=1" not in msg


def test_deprecated_default_invalid_parameter():

    with pytest.raises(ValueError):

        @deprecated_default(
            from_v="0.2.0", to_v="0.5.0", depr_param="x1", alt_value=999
        )
        def f(x=1):
            return x


def test_deprecated_default_with_message(recwarn):
    @deprecated_default(
        from_v="0.2.0",
        to_v="0.5.0",
        depr_param="arg11",
        alt_value="None",
        message="This is a message",
    )
    def f(arg11=1):
        pass

    f(arg11=3)
    msg = _get_warning_msg(recwarn)
    assert "This is a message" in msg


def test_deprecated_fn(recwarn):
    @deprecated_fn(
        from_v="0.2.0",
        to_v="0.5.0",
        alt_fn="my_alt_fn",
    )
    def f():
        pass

    f()
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "my_alt_fn" in msg


def test_deprecated_fn_with_message(recwarn):
    @deprecated_fn(
        from_v="0.2.0",
        to_v="0.5.0",
        alt_fn="my_alt_fn",
        message="This is a message",
    )
    def f():
        pass

    f()
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "my_alt_fn" in msg
    assert "This is a message" in msg


def test_deprecated_param_with_arg_input(recwarn):
    @deprecated_param(from_v="0.2.0", to_v="0.5.0", depr_param="arg11")
    def f(a, b, arg11=3, arg12=1):
        pass

    f(1, 2, 3)
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg


def test_deprecated_param_with_arg_input2(recwarn):
    @deprecated_param(from_v="0.2.0", to_v="0.5.0", depr_param="arg12")
    def f(a, b, arg11=3, arg12=1):
        pass

    f(1, 2, 3)
    with pytest.raises(AssertionError):
        _get_warning_msg(recwarn)


def test_deprecated_param_with_arg_input3(recwarn):
    @deprecated_param(from_v="0.2.0", to_v="0.5.0", depr_param="arg13")
    def f(a, b, arg11=3, arg12=1, arg13=1):
        pass

    f(1, 2, 3, arg13=10)
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg13" in msg


def test_deprecated_param_with_kwarg_input(recwarn):
    @deprecated_param(from_v="0.2.0", to_v="0.5.0", depr_param="arg11")
    def f(arg11=1):
        pass

    f(arg11=10)
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg


def test_deprecated_param_without_input(recwarn):
    @deprecated_param(from_v="0.2.0", to_v="0.5.0", depr_param="arg11")
    def f(arg11=1):
        pass

    f()
    with pytest.raises(AssertionError):
        _get_warning_msg(recwarn)


def test_deprecated_param_with_alt_argument(recwarn):
    @deprecated_param(
        from_v="0.2.0", to_v="0.5.0", depr_param="arg11", alt_param="arg12"
    )
    def f(arg11=1, arg12=1):
        pass

    f(arg11=3)
    msg = _get_warning_msg(recwarn)
    assert "0.2.0" in msg
    assert "0.5.0" in msg
    assert "arg11" in msg
    assert "arg12" in msg


def test_deprecated_param_with_alt_argument_not_found():

    with pytest.raises(ValueError):

        @deprecated_param(
            from_v="0.2.0", to_v="0.5.0", depr_param="arg11", alt_param="arg12"
        )
        def f(arg11=1):
            pass


def test_deprecated_param_with_message(recwarn):
    @deprecated_param(
        from_v="0.2.0",
        to_v="0.5.0",
        depr_param="arg11",
        message="This is a message",
    )
    def f(arg11=1):
        pass

    f(arg11=3)
    msg = _get_warning_msg(recwarn)
    assert "This is a message" in msg
