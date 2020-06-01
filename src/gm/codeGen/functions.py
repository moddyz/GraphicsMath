"""
A collection of classes serving as contextual objects used in the code-gen templates.
"""

from utils import UpperCamelCase
from collections import OrderedDict


class Mutability:
    """
    Describes the mutability of a function argument.
    """

    Const = 0
    Mutable = 1


class FunctionArg:
    """
    Description of a function argument.

    Args:
        key (str): key of this argument.
        type (ValueType): type of the argument.
        mutability (Mutability): mutability of the argument.
    """

    def __init__(self, key, type, mutability):
        self.key = key
        self.type = type
        self.mutability = mutability

    @property
    def constQualifier(self):
        if self.mutability == Mutability.Const:
            return "const"
        else:
            return ""

    @property
    def name(self):
        """
        Get the named identifier of this argument when it is used as an argument to a function.
        """
        if self.mutability == Mutability.Const:
            return "i_" + self.key
        else:
            return "o_" + self.key


class FunctionInterface:
    """
    Interface of a function, describing the arguments (type and qualifiers), and return type.

    Args:
        arguments (list): ordered list of function arguments.
        returnType (ValueType): return value type.  If `None` is specified, then the function return type is void.
    """

    def __init__(self, arguments, returnType=None):
        self._arguments = OrderedDict([(arg.key, arg) for arg in arguments])
        self._returnType = returnType

    @property
    def returnType(self):
        if self._returnType:
            return self._returnType.className
        else:
            return "void"

    @property
    def typedArgs(self):
        """
        Generate a string of typed, and named arguments.
        """

        def typedArg(arg):
            return "{constQualifier} {className}& {name}".format(
                constQualifier=arg.constQualifier,
                className=arg.type.className,
                name=arg.name,
            )

        return ", ".join([typedArg(arg) for arg in self._arguments.values()])

    @property
    def namedArgs(self):
        return ", ".join([arg.name for arg in self._arguments.values()])

    def Arg(self, key):
        """
        Retrieve a ``FunctionArg` from this interface, by key.
        """
        return self._arguments[key]

    def ArgVariable(self, key):
        """
        Convenience function to get the variable prefix of a argument called ``key``.

        Equivalent to Arg("``key``").type.variablePrefix.

        The following command performs the search and replacement.
        ```
        find . -key ".git" -prune -o -type f -exec sed -i 's/Arg("\([a-zA-Z]\+\)").type.variablePrefix/ArgVariable("\1")/g' {} +
        ```
        """
        return self._arguments[key].type.variablePrefix

    def ArgName(self, key):
        """
        Convenience function to get the argument key of a argument called ``key``.

        Equivalent to Arg("``key``").name.
        """
        return self._arguments[key].name

    def ArgClass(self, key):
        """
        Convenience function to get the type class key of a argument called ``key``.

        Equivalent to Arg("``key``").type.className.
        """
        return self._arguments[key].type.className


class Function:
    """
    A simple code-gen context object for a function.

    Args:
        name (str): name of the function.
        interfaces (list): list of interfaces which describe the different variations of
            arguments and return types.
    """

    def __init__(self, name, interfaces):
        self._name = name
        self.interfaces = interfaces

    @property
    def headerFileName(self):
        """
        Get the name of the header hosting this function.
        """
        return "{name}.h".format(name=self._name,)

    @property
    def name(self):
        """
        Returns:
            str: the C++ symbol name of this function.
        """
        return UpperCamelCase(self._name)

    @property
    def types(self):
        """
        Return:
            set: the unique set of types used across all interfaces of this function.
        """
        types = set()
        for interface in self.interfaces:
            types = types.union(
                [arg.type for arg in interface._arguments.values()]
            )
            if interface._returnType:
                types = types.union([interface._returnType])
        return types


class FunctionGroup:
    """
    Group of functions which share a common code-generation context.
    """

    def __init__(self, functionNames, interfaces):
        self.functions = []
        for name in functionNames:
            function = Function(name, interfaces)
            self.functions.append(function)
