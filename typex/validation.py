##########################################################################
# NSAp - Copyright (C) CEA, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from typing import Callable

from traits.api import HasTraits, TraitError

from .traits_extension import TRAIT_TYPES, traits  # noqa: F401


def check_type(
        val: object,
        func: Callable,
        name: str):
    """ Check if the input value have the correct type.

    Parameters
    ----------
    val: object
        the input value to check.
    func: callable
        a function with annotated parameters.
    name: str
        the name of the function parameter from which to retrieve the
        parameter specification.

    Raises
    ------
    TypeError
        If function parameters are not annotated.
    TraitError
        If the input value have incorrect type.
    NotImplementedError
        If a type is not handled by the code.
    """
    annotations = func.__annotations__
    if name not in annotations:
        raise TypeError(
            f"No '{name}' annotated parameter is defined on your "
            f"{func.__name__} function.")
    typing_type = annotations[name]
    traits_type_str = typing_to_traits(typing_type)
    traits_inst = eval(traits_type_str)
    signature = Signature()
    signature.add_trait(name, traits_inst)
    try:
        setattr(signature, name, val)
    except TraitError as exc:
        raise TraitError(
            f"The '{name}' parameter of the '{func.__name__}' function must "
            f" be a '{typing_type}', but a value of '{val}' was "
            "specified.") from exc


def typing_to_traits(annot, default_value=False):
    if hasattr(annot, "__name__"):
        name = f"{annot.__module__}.{annot.__name__}"
        name = name.replace("builtins.", "")
    else:
        name = repr(annot).split("[")[0]
    if name not in TRAIT_TYPES:
        raise NotImplementedError(f"The '{name}' type is not handled yet.")
    expr = f"{TRAIT_TYPES[name]}("
    if default_value:
        expr += "default_value=None, "
    if hasattr(annot, "__args__"):
        for sub_annot in annot.__args__:
            expr += typing_to_traits(sub_annot)
            expr += ", "
    expr += ")"
    return expr


class Signature(HasTraits):
    pass
