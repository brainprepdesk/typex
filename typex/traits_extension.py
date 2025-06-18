##########################################################################
# NSAp - Copyright (C) CEA, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import os

import numpy as np
import torch
import traits.api as traits


class Int(traits.BaseInt):
    def validate(self, objekt, name, value):
        if isinstance(value, bool):
            self.error(objekt, name, value)
        return super().validate(objekt, name, value)


class Float(traits.BaseFloat):
    def validate(self, objekt, name, value):
        if isinstance(value, int):
            self.error(objekt, name, value)
        return super().validate(objekt, name, value)


class Tuple(traits.BaseTuple):
    def validate(self, objekt, name, value):
        if isinstance(value, list):
            value = tuple(value)
        return super().validate(objekt, name, value)


class Array(traits.Array):
    def validate(self, objekt, name, value):
        if not isinstance(value, np.ndarray):
            self.error(objekt, name, value)
        return value


class Tensor(traits.TraitType):
    def validate(self, objekt, name, value):
        if not isinstance(value, torch.Tensor):
            self.error(objekt, name, value)
        return value


class File(traits.TraitType):
    def validate(self, objekt, name, value):
        if not (isinstance(value, str) and os.path.isfile(value)):
            self.error(objekt, name, value)
        return value


class Directory(traits.TraitType):
    def validate(self, objekt, name, value):
        if not (isinstance(value, str) and os.path.isdir(value)):
            self.error(objekt, name, value)
        return value


class Sequence(traits.List):
    def validate(self, objekt, name, value):
        if not isinstance(value, (tuple, list)):
            value = [value]
        if not isinstance(value, list):
            value = list(value)
        value = super().validate(objekt, name, value)
        if value:
            return value
        self.error(objekt, name, value)


class Undefined(traits.TraitType):
    def validate(self, objekt, name, value):
        if value is not None:
            self.error(objekt, name, value)
        return value


traits.Int = Int
traits.Float = Float
traits.Str = traits.Unicode
traits.Tuple = Tuple
traits.List = Tuple
traits.Array = Array
traits.Tensor = Tensor
traits.Sequence = Sequence
traits.Undefined = Undefined


TRAIT_TYPES = {
    "str": "traits.Str",
    "int": "traits.Int",
    "float": "traits.Float",
    "bool": "traits.Bool",
    "torch.Tensor": "traits.Tensor",
    "list": "traits.List",
    "tuple": "traits.Tuple",
    "collections.abc.Sequence": "traits.Sequence",
    "typing.Sequence": "traits.Sequence",
    "numpy.array": "traits.Array",
    "typing.Union": "traits.Union",
    "typing.Optional": "traits.Either",
    "NoneType": "traits.Undefined",
    "typex.typing_extensions.File": "traits.File",
    "typex.typing_extensions.Directory": "traits.Directory"
}
