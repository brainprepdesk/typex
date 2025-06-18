##########################################################################
# NSAp - Copyright (C) CEA, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


import inspect
from functools import wraps

from .validation import check_type


def typecheck(hints_params=True, hints_return=False):
    """ Enforce type hints on the parameters and return types of the decorated
    function.

    Parameters
    ----------
    hints_params: bool, default=False
        Require all parameter type hints to be specified.
    hints_return: bool, default=False 
        Require the return type hint to be specified.
    """
    def decorator(func):
        checker = TypEx(
            func,
            hints_params=hints_params,
            hints_return=hints_return
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            checker.check_params(args, kwargs)
            result = func(*args, **kwargs)
            checker.check_output(result)
            return result
        return wrapper
    return decorator


class TypEx:
    """ Enforce type hints on a function.

    Parameters
    ----------
    func: Callable
        The function whose type hints should be enforced.
    hints_params: bool, default=False
        Require all parameter type hints to be specified.
    hints_return: bool, default=False
        Require the return type hint to be specified.

    Raises
    ------
    TypeError
        If function parameters are not annotated.
    TraitError
        If the input value have incorrect type.
    NotImplementedError
        If a type is not handled by the code.
    """
    def __init__(self, func, hints_params=False, hints_return=False):
        self.func = func
        self.hints_params = hints_params
        self.hints_return = hints_return
        self.annotations = self.func.__annotations__
        param_names = list(inspect.signature(func).parameters.keys())
        self.ignore_self = (len(param_names) > 0 and param_names[0] == "self")
        self.n_params = (len(self.annotations)
                         if "return" not in self.annotations
                         else len(self.annotations) - 1)
        if self.hints_return and "return" not in self.annotations:
            raise TypeError(
                f"The return outputs of the '{func.__name__}' function is not "
                "annotated."
            )

    def check_params(self, passed_args, passed_kwargs):
        """ Check input function parameters.

        Parameters
        ----------
        passed_args: list
            List of args passed to the function
        passed_kwargs: dict
            Dict of kwargs passed to the function

        Raises
        ------
        TypeError
            If an input parameter is not valid.
        """
        if self.n_params < len(passed_args):
            raise TypeError(
                "Unexpected number of parameters for the "
                f"{self.func.__name__} function."
            )
        named_args = list(self.annotations.keys())[:len(passed_args)]
        if self.ignore_self:
            passed_args = passed_args[1:] 
        for name, val in zip(named_args, passed_args):
            check_type(val, self.func, name)
        for name, val in passed_kwargs.items():
            check_type(val, self.func, name)

    def check_output(self, value):
        """ Check return value of the function call.

        Parameters
        ----------
        value: Any
            The return value of the function.
        """
        check_type(value, self.func, "return")
