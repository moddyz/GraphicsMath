"""
A collection of classes serving as contextual objects used in the code gen templates.
"""


import os
import functools
import collections

from utils import LowerCamelCase, UpperCamelCase

"""
POD types we are interested in generating code for.  Double is omitted for the time being.
"""
FLOAT = "float"
DOUBLE = "double"
INT = "int"


class ValueType:
    """
    Abstract base class for all data types.
    """

    @property
    def className(self):
        raise NotImplementedError()

    @property
    def headerFileName(self):
        raise NotImplementedError()

    @property
    def isScalar(self):
        return False

    @property
    def isVector(self):
        return False

    @property
    def isArray(self):
        return False

    @property
    def isComposite(self):
        return False


class PODType(ValueType):
    """
    POD (Plain old data) type, used in code-gen contexts.
    """

    def __init__(self, typeName):
        assert isinstance(typeName, str)
        self._typeName = typeName

    def __hash__(self):
        return hash((self._typeName))

    @property
    def className(self):
        """
        Returns:
            str: the ctype of this type.
        """
        return self._typeName

    @property
    def isScalar(self):
        return True

    def CppNumber(self, value):
        """
        Convert a numeric value ``value`` to the corresponding C++ compliant value as a string.
        """
        if self.className == INT:
            return str(int(value))
        elif self.className == FLOAT:
            return str(float(value)) + "f"
        elif self.className == DOUBLE:
            return str(float(value))


class VectorType(ValueType):
    """
    Code generation for an C++ vector type.
    """

    def __init__(self, dims, elementType):
        assert isinstance(dims, tuple)
        assert isinstance(elementType, PODType)
        self.dims = dims
        self.elementType = elementType

    def __hash__(self):
        return hash((self.dims, self.elementType))

    @property
    def elementSize(self):
        return functools.reduce(lambda x, y: x * y, self.dims)

    @property
    def variablePrefix(self):
        """
        Returns:
            str: a meaningful prefix for naming variables of this type.
        """
        if len(self.dims) == 2:
            return "matrix"
        else:
            return "vector"

    @property
    def className(self):
        if len(self.dims) == 2:
            prefix = "Mat"
        else:
            prefix = "Vec"

        return "{prefix}{dims}{elementType}".format(
            prefix=prefix,
            dims=str(self.dims[0]),
            elementType=self.elementType.className[0],
        )

    @property
    def headerFileName(self):
        if len(self.dims) == 2:
            prefix = "mat"
        else:
            prefix = "vec"

        return "{prefix}{dims}{elementType}.h".format(
            prefix=prefix,
            dims=str(self.dims[0]),
            elementType=self.elementType.className[0],
        )

    @property
    def isVector(self):
        return True

    def CppNumber(self, value):
        """
        Convert a numeric value ``value`` to the corresponding C++ compliant value as a string.
        """
        return self.elementType.CppNumber(value)

    def PyNumber(self, value):
        """
        Convert a numeric value ``value`` to the corresponding C++ compliant value as a string.
        """
        if self.elementType.className == INT:
            return str(int(value))
        elif self.elementType.className in (FLOAT, DOUBLE):
            return str(float(value))


class ArrayType(ValueType):
    """
    Code generation for an C++ array type.
    """

    def __init__(self, elementType):
        assert isinstance(elementType, ValueType)
        self.elementType = elementType

    def __hash__(self):
        return hash((self.elementType, "Array"))

    @property
    def className(self):
        return "{elementTypeName}Array".format(
            elementTypeName=(UpperCamelCase(self.elementType.className))
        )

    @property
    def headerFileName(self):
        if self.elementType.isVector:
            return "{elementHeaderFileName}Array.h".format(
                elementHeaderFileName=os.path.splitext(self.elementType.headerFileName)[
                    0
                ]
            )
        else:
            return "{elementTypeName}Array.h".format(
                elementTypeName=LowerCamelCase(self.elementType.className),
            )

    @property
    def isArray(self):
        return True


class CompositeElement:
    """
    CompositeElement is a single element of an CompositeType, described by a name, type, and default value.

    Args:
        name (str): is used to uniquely address this element from the parent Composite type.
        type (object): the data type.
        defaultValue (str): string, encoding C++ code that will be assigned to element member variable.
    """

    def __init__(self, name, type, defaultValue):
        self.name = name
        self.type = type
        self.defaultValue = defaultValue

    @property
    def accessorName(self):
        return UpperCamelCase(self.name)


class CompositeType(ValueType):
    """
    Code generation for an C++ composite data type.
    A composite type is a structure composed of one or more elements.
    Each element can be of type pod, vector, array, or another composite.

    Args:
        name (str): name of the composite type.
        elements (list): list of CompositeElement(s).
        extraIncludes (list): list of extras includes to encode near the top of the source file.
    """

    def __init__(self, name, elements, extraIncludes=None):
        for element in elements:
            assert isinstance(element.type, ValueType)
        self._name = name
        self.elements = elements
        self.elementSize = len(self.elements)
        self.extraIncludes = extraIncludes or []

    def __hash__(self):
        return hash((self._name, self.elements))

    @property
    def className(self):
        return UpperCamelCase(self._name)

    @property
    def headerFileName(self):
        return "{name}.h".format(name=LowerCamelCase(self._name),)

    @property
    def isComposite(self):
        return True
