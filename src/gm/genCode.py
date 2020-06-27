#!/usr/bin/env python

"""
Main entry point / script for generating GraphicsMath C++ code from templates.
"""

import os

from codeGen.utils import (
    GetTemplateFile,
    GenerateCode,
    WriteFile,
    FormatCode,
    LowerCamelCase,
    UpperCamelCase,
)

from codeGen.types import (
    PODType,
    VectorType,
    ArrayType,
    CompositeType,
    CompositeElement,
    INT,
    FLOAT,
    BOOL,
)

from codeGen.functions import (
    FunctionGroup,
    Function,
    FunctionInterface,
    FunctionArg,
    Mutability,
)


"""
Name of the subdirectory where all type header files reside.
"""
TYPES_DIR = "types"

"""
Name of the subdirectory where all function header files reside.
"""
FUNCTIONS_DIR = "functions"

"""
Name of the subdirectory, under types/ and functions/ where their tests reside.
"""
TESTS_DIR = "tests"

"""
Name of the benchmarks sub-directory, under functions/, where benchmarking code reside.
"""
BENCHMARKS_DIR = "benchmarks"

"""
Name of the python subdirectory, where the bindings reside.
"""
PYTHON_DIR = "python"

"""
Global set of POD value types.
"""
NUMERIC_POD_TYPES = [PODType(FLOAT), PODType(INT)]
POD_TYPES = NUMERIC_POD_TYPES + [PODType(BOOL)]

"""
Global set of vector value types to generate.
"""
MATRIX_TYPES = [
    VectorType((3, 3), PODType(FLOAT)),
    VectorType((4, 4), PODType(FLOAT)),
]

SINGLE_INDEX_VECTOR_TYPES_FLOAT = [
    VectorType((2,), PODType(FLOAT)),
    VectorType((3,), PODType(FLOAT)),
    VectorType((4,), PODType(FLOAT)),
]

SINGLE_INDEX_VECTOR_TYPES_INT = [
    VectorType((2,), PODType(INT)),
    VectorType((3,), PODType(INT)),
    VectorType((4,), PODType(INT)),
]

VECTOR_TYPES = sorted(
    SINGLE_INDEX_VECTOR_TYPES_FLOAT + SINGLE_INDEX_VECTOR_TYPES_INT + MATRIX_TYPES
)

"""
COMPOSITE_TYPES is a dict of type name (str) -> type object (CompositeType).
It is populated in GenerateCompositeTypes.
"""
COMPOSITE_TYPES = {}

"""
FUNCTIONS is a dict of function name (str) -> function object (Function).
It is populated in GenerateFunctions.
"""
FUNCTIONS = {}

#
# Code generation for types.
#

def PopulateBoundsCompositeTypes():
    """
    Populate bounds composite types, by updating the global ``COMPOSITE_TYPES``.
    """
    filePaths = []

    for vectorType in [
        VectorType((2,), PODType(FLOAT)),
        VectorType((3,), PODType(FLOAT)),
        VectorType((2,), PODType(INT)),
        VectorType((3,), PODType(INT)),
    ]:
        compositeTypeName = "bounds{dims}{elementType}".format(
            dims=str(vectorType.dims[0]),
            elementType=vectorType.elementType.className[0],
        )

        # Min default value.
        minDefaultValue = "{vectorClassName}(".format(
            vectorClassName=vectorType.className
        )
        for index in range(vectorType.dims[0]):
            minDefaultValue += "std::numeric_limits< {vectorElementType} >::max()".format(
                vectorElementType=vectorType.elementType.className
            )
            if index + 1 < vectorType.dims[0]:
                minDefaultValue += ","
        minDefaultValue += ")"

        # Max default value.
        maxDefaultValue = "{vectorClassName}(".format(
            vectorClassName=vectorType.className
        )
        for index in range(vectorType.dims[0]):
            maxDefaultValue += "std::numeric_limits< {vectorElementType} >::min()".format(
                vectorElementType=vectorType.elementType.className
            )
            if index + 1 < vectorType.dims[0]:
                maxDefaultValue += ","
        maxDefaultValue += ")"

        # Instantiate the type with min-max elements.
        compositeType = CompositeType(
            compositeTypeName,
            [
                CompositeElement(
                    name="min", type=vectorType, defaultValue=minDefaultValue
                ),
                CompositeElement(
                    name="max", type=vectorType, defaultValue=maxDefaultValue
                ),
            ],
            extraIncludes=["<limits>",],
        )

        # Store composite type into global COMPOSITE_TYPES, to be queried in function generation
        # in a later stage.
        COMPOSITE_TYPES[compositeType.className] = compositeType

    return filePaths


def GenerateCompositeTypes():
    """
    Generate all composite type source files.

    Returns:
        list: paths to generated source files.
    """
    PopulateBoundsCompositeTypes()

    # Generate C++ source code.
    filePaths = []

    for compositeType in COMPOSITE_TYPES.values():
        # C++ source code.
        filePaths.append(
            GenerateCode(
                os.path.join(TYPES_DIR, "compositeType.h"),
                os.path.join(TYPES_DIR, compositeType.headerFileName),
                compositeType=compositeType,
            )
        )

        # Python bindings.
        filePaths.append(
            GenerateCode(
                os.path.join(PYTHON_DIR, TYPES_DIR, "bindCompositeType.cpp"),
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    "bind{className}.cpp".format(className=compositeType.className),
                ),
                compositeType=compositeType,
            )
        )

        # Tests for python bindings.
        filePaths.append(
            GenerateCode(
                os.path.join(PYTHON_DIR, TYPES_DIR, TESTS_DIR, "testCompositeType.py"),
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    TESTS_DIR,
                    "test{className}.py".format(className=compositeType.className),
                ),
                compositeType=compositeType,
            )
        )

    return filePaths


def GenerateArrayTypes():
    """
    Generate all array type source files.

    Returns:
        list: paths to generated source files.
    """
    # Build ArrayType(s)
    arrayTypes = []
    for podType in POD_TYPES:
        arrayType = ArrayType(podType)
        arrayTypes.append(arrayType)

    for vectorType in VECTOR_TYPES:
        arrayType = ArrayType(vectorType)
        arrayTypes.append(arrayType)

    # Generate code for ArrayType(s)
    filePaths = []
    for arrayType in arrayTypes:
        filePaths.append(
            GenerateCode(
                os.path.join(TYPES_DIR, "arrayType.h"),
                os.path.join(TYPES_DIR, arrayType.headerFileName),
                arrayType=arrayType,
            )
        )

    return filePaths


def GenerateVectorTypes():
    """
    Generate all vector type source files.

    Returns:
        list: paths to generated source files.
    """
    # Generate vector class headers.
    filePaths = []
    for vectorType in VECTOR_TYPES:
        # C++ header source.
        filePaths.append(
            GenerateCode(
                os.path.join(TYPES_DIR, "vectorType.h"),
                os.path.join(TYPES_DIR, vectorType.headerFileName),
                vectorType=vectorType,
            )
        )

        # C++ tests.
        filePaths.append(
            GenerateCode(
                os.path.join(TYPES_DIR, TESTS_DIR, "testVectorType.cpp"),
                os.path.join(
                    TYPES_DIR,
                    TESTS_DIR,
                    "test{className}.cpp".format(className=vectorType.className),
                ),
                vectorType=vectorType,
            )
        )

        # Python bindings source.
        filePaths.append(
            GenerateCode(
                os.path.join(PYTHON_DIR, TYPES_DIR, "bindVectorType.cpp"),
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    "bind{className}.cpp".format(className=vectorType.className),
                ),
                vectorType=vectorType,
            )
        )

        # Python bindings tests.
        filePaths.append(
            GenerateCode(
                os.path.join(PYTHON_DIR, TYPES_DIR, TESTS_DIR, "testVectorType.py"),
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    TESTS_DIR,
                    "test{className}.py".format(className=vectorType.className),
                ),
                vectorType=vectorType,
            )
        )

    return filePaths


def GenerateTypes():
    """
    Top-level entry point for generating all data type source files.
    Vectors and matrices types will be generated.
    Array types of pod, vectors, and matrices will also be generated.

    Returns:
        list: paths to of generated source files.
    """
    filePaths = GenerateVectorTypes()
    filePaths += GenerateArrayTypes()
    filePaths += GenerateCompositeTypes()
    return filePaths


#
# Code generation for functions.
#


def GenerateFunctions():
    """
    Generate code for all of the functions.

    Returns:
        list: file paths to the generated files.
    """
    # Unary operations.
    unaryOps = []
    for valueType in [PODType(FLOAT),] + SINGLE_INDEX_VECTOR_TYPES_FLOAT + MATRIX_TYPES:
        unaryOps.append(
            FunctionInterface(
                arguments=[FunctionArg("value", valueType, Mutability.Const),],
                returnType=valueType,
            )
        )

    # Binary comparison operations.
    binaryComparisonOps = []
    for valueType in POD_TYPES + VECTOR_TYPES:
        binaryComparisonOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("valueA", valueType, Mutability.Const),
                    FunctionArg("valueB", valueType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    # Vector product(s).
    vectorProductOps = []
    for vectorType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        vectorProductOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", vectorType, Mutability.Const),
                    FunctionArg("rhs", vectorType, Mutability.Const),
                ],
                returnType=vectorType.elementType,
            )
        )

    # Vector reduction.
    vectorReductionOps = []
    for vectorType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        vectorReductionOps.append(
            FunctionInterface(
                arguments=[FunctionArg("vector", vectorType, Mutability.Const),],
                returnType=vectorType.elementType,
            )
        )

    # Vector unary operation.
    vectorOps = []
    for vectorType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        vectorOps.append(
            FunctionInterface(
                arguments=[FunctionArg("vector", vectorType, Mutability.Const),],
                returnType=vectorType,
            )
        )

    # Set matrix value.
    setMatrixOps = []
    for matrixType in MATRIX_TYPES:
        setMatrixOps.append(
            FunctionInterface(
                arguments=[FunctionArg("matrix", matrixType, Mutability.Mutable),],
            )
        )

    # Check matrix value.
    checkMatrixOps = []
    for matrixType in MATRIX_TYPES:
        checkMatrixOps.append(
            FunctionInterface(
                arguments=[FunctionArg("matrix", matrixType, Mutability.Const),],
                returnType=PODType(BOOL),
            )
        )

    # Matrix unary ops.
    matrixUnaryOps = []
    for matrixType in MATRIX_TYPES:
        matrixUnaryOps.append(
            FunctionInterface(
                arguments=[FunctionArg("matrix", matrixType, Mutability.Const),],
                returnType=matrixType,
            )
        )

    # Matrix binary ops.
    matrixBinaryOps = []
    for matrixType in MATRIX_TYPES:
        matrixBinaryOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", matrixType, Mutability.Const),
                    FunctionArg("rhs", matrixType, Mutability.Const),
                ],
                returnType=matrixType,
            )
        )

    # Set vector transform channels.
    setVectorTransformOps = []
    for matrixType in MATRIX_TYPES:
        setVectorTransformOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("vector", VectorType((matrixType.dims[0] - 1,), matrixType.elementType), Mutability.Const),
                    FunctionArg("matrix", matrixType, Mutability.Mutable),
                ],
            )
        )

    # Angle interfaces.
    angleOps = []
    for podType in (PODType(FLOAT),):
        angleOps.append(
            FunctionInterface(
                arguments=[FunctionArg("angle", podType, Mutability.Const),],
                returnType=podType,
            )
        )

    # Euclidean space point operations.
    pointReductionOps = []
    for vectorType in (
        VectorType((2,), PODType(FLOAT)),
        VectorType((3,), PODType(FLOAT)),
    ):
        pointReductionOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("pointA", vectorType, Mutability.Const),
                    FunctionArg("pointB", vectorType, Mutability.Const),
                ],
                returnType=vectorType.elementType,
            )
        )

    # Interpolation operators.
    interpolationOps = []
    for valueType in [PODType(FLOAT)] + MATRIX_TYPES + SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        arguments = [
            FunctionArg("valueA", valueType, Mutability.Const),
            FunctionArg("valueB", valueType, Mutability.Const),
        ]
        if valueType.isScalar:
            arguments.append(FunctionArg("weight", valueType, Mutability.Const))
        else:
            assert(valueType.isVector)
            arguments.append(FunctionArg("weight", valueType.elementType, Mutability.Const))

        interpolationOps.append(
            FunctionInterface(
                arguments=arguments,
                returnType=valueType,
            )
        )

    rayOps = []
    for valueType in (VectorType((2,), PODType(FLOAT)), VectorType((3,), PODType(FLOAT)),):
        rayOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("origin", valueType, Mutability.Const),
                    FunctionArg("direction", valueType, Mutability.Const),
                    FunctionArg("magnitude", valueType.elementType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    quadraticOps = []
    for valueType in (PODType(FLOAT),):
        quadraticOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("a", valueType, Mutability.Const),
                    FunctionArg("b", valueType, Mutability.Const),
                    FunctionArg("c", valueType, Mutability.Const),
                    FunctionArg("firstRoot", valueType, Mutability.Mutable),
                    FunctionArg("secondRoot", valueType, Mutability.Mutable),
                ],
                returnType=PODType(INT),
            )
        )

    raySphereIntersectionOps = []
    for valueType in (VectorType((3,), PODType(FLOAT)),):
        raySphereIntersectionOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("sphereOrigin", valueType, Mutability.Const),
                    FunctionArg("sphereRadius", valueType.elementType, Mutability.Const),
                    FunctionArg("rayOrigin", valueType, Mutability.Const),
                    FunctionArg("rayDirection", valueType, Mutability.Const),
                    FunctionArg("firstIntersection", valueType.elementType, Mutability.Mutable),
                    FunctionArg("secondIntersection", valueType.elementType, Mutability.Mutable),
                ],
                returnType=PODType(INT),
            )
        )

    functionGroups = [
        FunctionGroup(["floor", "ceil", "abs",], interfaces=unaryOps),
        FunctionGroup(["min", "max",], interfaces=binaryComparisonOps,),
        FunctionGroup(["isIdentity"], interfaces=checkMatrixOps,),
        FunctionGroup(["setIdentity"], interfaces=setMatrixOps,),
        FunctionGroup(["transpose"], interfaces=matrixUnaryOps,),
        FunctionGroup(["matrixProduct"], interfaces=matrixBinaryOps,),
        FunctionGroup(["normalize",], interfaces=vectorOps,),
        FunctionGroup(["length", "lengthSquared",], interfaces=vectorReductionOps,),
        FunctionGroup(["dotProduct"], interfaces=vectorProductOps,),
        FunctionGroup(["degrees", "radians",], interfaces=angleOps,),
        FunctionGroup(["distance"], interfaces=pointReductionOps,),
        FunctionGroup(["setTranslate", "setScale",], interfaces=setVectorTransformOps,),
        FunctionGroup(["lerp",], interfaces=interpolationOps,),
        FunctionGroup(["solveQuadraticRoots",], interfaces=quadraticOps,),
        FunctionGroup(["rayPosition",], interfaces=rayOps,),
        FunctionGroup(["raySphereIntersection",], interfaces=raySphereIntersectionOps,),
    ]

    # Generate code.
    filePaths = []
    for functionGroup in functionGroups:
        for function in functionGroup.functions:
            # Generate C++ source code.
            filePaths.append(
                GenerateCode(
                    os.path.join(FUNCTIONS_DIR, function.headerFileName),
                    os.path.join(FUNCTIONS_DIR, function.headerFileName),
                    function=function,
                )
            )

            # Generate C++ test code (if the template is available).
            # Some tests are hand-authored.
            testTemplatePath = os.path.join(
                FUNCTIONS_DIR, TESTS_DIR, "test{name}.cpp".format(name=function.name)
            )
            if os.path.isfile(GetTemplateFile(testTemplatePath)):
                filePaths.append(
                    GenerateCode(
                        testTemplatePath,
                        os.path.join(
                            FUNCTIONS_DIR,
                            TESTS_DIR,
                            "test{name}.cpp".format(name=function.name),
                        ),
                        function=function,
                    )
                )

            # Benchmarking.
            filePaths.append(
                GenerateCode(
                    os.path.join(
                        FUNCTIONS_DIR, BENCHMARKS_DIR, "benchmarkFunction.cpp"
                    ),
                    os.path.join(
                        FUNCTIONS_DIR,
                        BENCHMARKS_DIR,
                        "benchmark{name}.cpp".format(name=function.name),
                    ),
                    function=function,
                )
            )

            # Python bindings source.
            filePaths.append(
                GenerateCode(
                    os.path.join(PYTHON_DIR, FUNCTIONS_DIR, "bindFunction.cpp"),
                    os.path.join(
                        PYTHON_DIR,
                        FUNCTIONS_DIR,
                        "bind{name}.cpp".format(name=function.name),
                    ),
                    function=function,
                )
            )

            # Register in global FUNCTIONS
            assert function.name not in FUNCTIONS
            FUNCTIONS[function.name] = function

    return filePaths


#
# Main
#

if __name__ == "__main__":
    # Generate types first, to populate type registry.
    filePaths = GenerateTypes()

    # Proceed with generating functions.
    filePaths += GenerateFunctions()

    # Generate python module.
    filePaths.append(
        GenerateCode(
            os.path.join(PYTHON_DIR, "module.cpp"),
            os.path.join(PYTHON_DIR, "module.cpp"),
            types=list(VECTOR_TYPES) + COMPOSITE_TYPES.values(),
            functions=FUNCTIONS.values(),
            UpperCamelCase=UpperCamelCase,
        )
    )

    # Format all the code to standard.
    FormatCode(filePaths)
