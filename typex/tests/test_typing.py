##########################################################################
# NSAp - Copyright (C) CEA, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import os
import torch
import types
import unittest


import numpy as np

from typing import Optional, Sequence, Union
from traits.api import TraitError
from typex.decorator import typecheck
from typex.validation import check_type
from typex.typing_extensions import File, Directory


class TestExperiment(unittest.TestCase):
    """ Test experiement.
    """
    def setUp(self):
        """ Setup test.
        """
        self.types = [
            int,
            float,
            bool,
            str,
            list[float, float],
            list[torch.Tensor],
            tuple[int, int],
            np.array,
        ]
        self.values = [
            3,
            2.3,
            True,
            "test",
            [2., 3.],
            [torch.zeros((5,))],
            [2, 3],
            np.zeros((5, )), 
        ]
        self.mtypes = [
            Union[int, float],
            Union[int, float],
            Sequence[int],
            Optional[int],
            File,
            Directory,
        ]
        self.mvalues = [
            (3, None),
            (2.3, None),
            ([1, 2, 3], None),
            (None, 3.),
            (__file__, None),
            (os.path.dirname(__file__), None),
        ]

    def tearDown(self):
        """ Run after each test.
        """
        pass

    def test_typecheck(self):
        """ Test type check.
        """
        for idx1, _type, in enumerate(self.types):
            print(f"[{repr(_type)}]...")
            _func = get_func(template_func, {"my_param": _type}, "test_func")
            for idx2, _val in enumerate(self.values):
                if idx1 == idx2:
                    check_type(_val, _func, "my_param")
                else:
                    try:
                        check_type(_val, _func, "my_param")
                        self.fail("Has to raise TraitError!")
                    except Exception as inst:
                        print(inst)
                        self.assertTrue(isinstance(inst, TraitError))

    def test_multi_typecheck(self):
        """ Test type check with choices.
        """
        for  _type, _vals in zip(self.mtypes, self.mvalues):
            print(f"[{repr(_type)}]...")
            _func = get_func(template_func, {"my_param": _type}, "test_func")
            check_type(_vals[0], _func, "my_param")
            try:
                check_type(_vals[1], _func, "my_param")
                self.fail("Has to raise TraitError!")
            except Exception as inst:
                print(inst)
                self.assertTrue(isinstance(inst, TraitError))

    def test_decorator(self):
        """ Test the decorator.
        """
        typecheck(hints_params=True, hints_return=True)(simple_sum)(1, b=2)
        try:
            typecheck(hints_params=True, hints_return=True)(simple_sum)(
                1., b=2)
            self.fail("Has to raise TraitError!")
        except Exception as inst:
            print(inst)
            self.assertTrue(isinstance(inst, TraitError))
        obj = SimpleClass()
        obj.simple_sum(1, b=2)
        try:
            obj.simple_sum(1., b=2)
            self.fail("Has to raise TraitError!")
        except Exception as inst:
            print(inst)
            self.assertTrue(isinstance(inst, TraitError))


def get_func(func, func_types, name=None):
    new_func = types.FunctionType(
        func.__code__, func.__globals__, name or func.__name__,
        func.__defaults__, func.__closure__)
    new_func.__annotations__ = func_types
    return new_func


def template_func(arg):
    pass


def simple_sum(a: int, b: int) -> int:
    return a + b


class SimpleClass:
    @typecheck(hints_params=True, hints_return=True)
    def simple_sum(self, a: int, b: int) -> int:
        return a + b


if __name__ == "__main__":
    unittest.main()
