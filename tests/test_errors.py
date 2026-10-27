import pytest

from app.errors import AppError


class _SpecificError(AppError):
    pass


def test_app_error_checked_as_exception_is_subclass():
    assert issubclass(AppError, Exception)


def test_app_error_raised_with_message_keeps_message():
    with pytest.raises(AppError, match="order 42 not found"):
        raise AppError("order 42 not found")


def test_app_error_subclass_is_caught_as_app_error():
    with pytest.raises(AppError):
        raise _SpecificError("specific failure")


def test_app_error_without_message_has_empty_text():
    assert str(AppError()) == ""
