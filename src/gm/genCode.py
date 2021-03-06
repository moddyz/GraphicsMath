#!/usr/bin/env python

"""
Main entry point / script for generating GraphicsMath C++ and Python source code from templates.
"""

import os
import argparse
import logging

from codeGen.utils import (
    GetTemplateFile,
    GenerateCode,
    WriteFile,
    FormatCode,
    LowerCamelCase,
    UpperCamelCase,
    PrintMessage,
    SetupLogging,
)

from codeGen.types import (
    ScalarType,
    VectorType,
    RangeType,
    CompositeType,
    NamedElement,
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
    FunctionCategory,
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
Global set of Scalar value types.
"""
NUMERIC_SCALAR_TYPES = [ScalarType(FLOAT), ScalarType(INT)]
SCALAR_TYPES = NUMERIC_SCALAR_TYPES + [ScalarType(BOOL)]

"""
Global set of vector value types to generate.
"""
MATRIX_TYPES = [
    VectorType((3, 3), ScalarType(FLOAT)),
    VectorType((4, 4), ScalarType(FLOAT)),
]

SINGLE_INDEX_VECTOR_TYPES_FLOAT = [
    VectorType((2,), ScalarType(FLOAT)),
    VectorType((3,), ScalarType(FLOAT)),
    VectorType((4,), ScalarType(FLOAT)),
]

SINGLE_INDEX_VECTOR_TYPES_INT = [
    VectorType((2,), ScalarType(INT)),
    VectorType((3,), ScalarType(INT)),
    VectorType((4,), ScalarType(INT)),
]

VECTOR_TYPES = SINGLE_INDEX_VECTOR_TYPES_FLOAT + SINGLE_INDEX_VECTOR_TYPES_INT + MATRIX_TYPES

"""
RANGE_TYPES is the fixed, global set of range-based types (min, max) to generate code for.
"""
RANGE_TYPES = [RangeType(scalarType) for scalarType in NUMERIC_SCALAR_TYPES] + [
    RangeType(vectorType) for vectorType in VECTOR_TYPES if len(vectorType.shape) == 1
]

RANGE_TYPES_VECTOR = [
    RangeType(valueType) for valueType in (SINGLE_INDEX_VECTOR_TYPES_FLOAT + SINGLE_INDEX_VECTOR_TYPES_INT)
]

RANGE_TYPES_FLOAT = [RangeType(valueType) for valueType in (SINGLE_INDEX_VECTOR_TYPES_FLOAT + [ScalarType(FLOAT)])]


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


def PopulateCompositeTypes():
    """
    Populate the COMPOSITE_TYPES dictionary.
    """
    compositeTypes = []
    for compositeType in compositeTypes:
        COMPOSITE_TYPES[compositeType.name] = compositeType


def GenerateTypes():
    """
    Top-level entry point for generating all data type source files.
    Vectors and matrices types will be generated.

    Returns:
        tuple: (
            list: paths to of generated source files.
            list: associated ValueType(s)
        )
    """
    PrintMessage("Generating types...")

    PopulateCompositeTypes()

    filePaths = []
    valueTypes = VECTOR_TYPES + RANGE_TYPES + COMPOSITE_TYPES.values()
    for valueType in valueTypes:
        # C++ source code.
        filePaths.append(
            GenerateCode(
                os.path.join(TYPES_DIR, "{category}Type.h".format(category=valueType.CATEGORY,)),
                os.path.join(TYPES_DIR, valueType.headerFileName),
                valueType=valueType,
            )
        )

        # Cpp tests.
        filePaths.append(
            GenerateCode(
                os.path.join(
                    TYPES_DIR, TESTS_DIR, "test{category}Type.cpp".format(category=UpperCamelCase(valueType.CATEGORY),),
                ),
                os.path.join(TYPES_DIR, TESTS_DIR, "test{className}.cpp".format(className=valueType.className),),
                valueType=valueType,
            )
        )

        # Python bindings.
        filePaths.append(
            GenerateCode(
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    "bind{category}Type.cpp".format(category=UpperCamelCase(valueType.CATEGORY),),
                ),
                os.path.join(PYTHON_DIR, TYPES_DIR, "bind{className}.cpp".format(className=valueType.className),),
                valueType=valueType,
            )
        )

        # Tests for python bindings.
        filePaths.append(
            GenerateCode(
                os.path.join(
                    PYTHON_DIR,
                    TYPES_DIR,
                    TESTS_DIR,
                    "test{category}Type.py".format(category=UpperCamelCase(valueType.CATEGORY),),
                ),
                os.path.join(
                    PYTHON_DIR, TYPES_DIR, TESTS_DIR, "test{className}.py".format(className=valueType.className),
                ),
                valueType=valueType,
            )
        )

    return filePaths, valueTypes


def GenerateFunctions():
    """
    Generate code for all of the functions.

    Returns:
        list: file paths to the generated files.
    """
    PrintMessage("Generating functions...")

    # Unary operations.
    unaryOps = []
    for valueType in [ScalarType(FLOAT),] + SINGLE_INDEX_VECTOR_TYPES_FLOAT + MATRIX_TYPES:
        unaryOps.append(
            FunctionInterface(arguments=[FunctionArg("value", valueType, Mutability.Const),], returnType=valueType,)
        )

    # Range unary operations.
    rangeUnaryOps = []
    for rangeType in RANGE_TYPES:

        if rangeType.elementType.isScalar:
            returnType = rangeType.elementType
        else:
            returnType = rangeType.elementType.elementType

        rangeUnaryOps.append(
            FunctionInterface(
                arguments=[FunctionArg("range", rangeType, Mutability.Const),],
                returnType=returnType,
            )
        )

    # Binary comparison operations.
    binaryComparisonOps = []
    for valueType in SCALAR_TYPES + VECTOR_TYPES:
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

    # Cross product.
    crossProductOps = []
    for vectorType in (VectorType((3,), ScalarType(FLOAT)),):
        crossProductOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", vectorType, Mutability.Const),
                    FunctionArg("rhs", vectorType, Mutability.Const),
                ],
                returnType=vectorType,
            )
        )

    # Coordinate system.
    coordSysOps = []
    for vectorType in (VectorType((3,), ScalarType(FLOAT)),):
        coordSysOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("vectorA", vectorType, Mutability.Const),
                    FunctionArg("vectorB", vectorType, Mutability.Mutable),
                    FunctionArg("vectorC", vectorType, Mutability.Mutable),
                ],
            )
        )

    # Vector reduction.
    vectorReductionOps = []
    for vectorType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        vectorReductionOps.append(
            FunctionInterface(
                arguments=[FunctionArg("vector", vectorType, Mutability.Const),], returnType=vectorType.elementType,
            )
        )

    # Vector unary operation.
    vectorOps = []
    for vectorType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        vectorOps.append(
            FunctionInterface(arguments=[FunctionArg("vector", vectorType, Mutability.Const),], returnType=vectorType,)
        )

    # Set matrix value.
    setMatrixOps = []
    for matrixType in MATRIX_TYPES:
        setMatrixOps.append(FunctionInterface(arguments=[FunctionArg("matrix", matrixType, Mutability.Mutable),],))

    # Check matrix value.
    checkMatrixOps = []
    for matrixType in MATRIX_TYPES:
        checkMatrixOps.append(
            FunctionInterface(
                arguments=[FunctionArg("matrix", matrixType, Mutability.Const),], returnType=ScalarType(BOOL),
            )
        )

    # Matrix unary ops.
    matrixUnaryOps = []
    for matrixType in MATRIX_TYPES:
        matrixUnaryOps.append(
            FunctionInterface(arguments=[FunctionArg("matrix", matrixType, Mutability.Const),], returnType=matrixType,)
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
                    FunctionArg(
                        "vector", VectorType((matrixType.shape[0] - 1,), matrixType.elementType), Mutability.Const,
                    ),
                    FunctionArg("matrix", matrixType, Mutability.Mutable),
                ],
            )
        )

    # Set rotation XYZ axis ops.
    setRotateXYZOps = []
    for matrixType in [VectorType((4, 4), ScalarType(FLOAT))]:
        setRotateXYZOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("angle", matrixType.elementType, Mutability.Const,),
                    FunctionArg("matrix", matrixType, Mutability.Mutable),
                ],
            )
        )

    # Set arbituary rotation operations.
    setRotateOps = []
    for matrixType in [VectorType((4, 4), ScalarType(FLOAT))]:
        setRotateOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("angle", matrixType.elementType, Mutability.Const,),
                    FunctionArg(
                        "axis", VectorType((matrixType.shape[0] - 1,), matrixType.elementType), Mutability.Const,
                    ),
                    FunctionArg("matrix", matrixType, Mutability.Mutable),
                ],
            )
        )

    # Angle interfaces.
    angleOps = []
    for scalarType in (ScalarType(FLOAT),):
        angleOps.append(
            FunctionInterface(arguments=[FunctionArg("angle", scalarType, Mutability.Const),], returnType=scalarType,)
        )

    # Euclidean space point operations.
    pointReductionOps = []
    for vectorType in (
        VectorType((2,), ScalarType(FLOAT)),
        VectorType((3,), ScalarType(FLOAT)),
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
    linearInterpolationOps = []
    for valueType in [ScalarType(FLOAT)] + MATRIX_TYPES + SINGLE_INDEX_VECTOR_TYPES_FLOAT + RANGE_TYPES_FLOAT:
        arguments = [
            FunctionArg("source", valueType, Mutability.Const),
            FunctionArg("target", valueType, Mutability.Const),
        ]

        if valueType.isScalar:
            weightType = valueType
        else:
            if valueType.elementType.isScalar:
                weightType = valueType.elementType
            else:
                weightType = valueType.elementType.elementType

        arguments.append(FunctionArg("weight", weightType, Mutability.Const))
        linearInterpolationOps.append(FunctionInterface(arguments=arguments, returnType=valueType,))

    bilinearInterpolationOps = []
    for valueType in [ScalarType(FLOAT)] + MATRIX_TYPES + SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        arguments = [
            FunctionArg("corner00", valueType, Mutability.Const),
            FunctionArg("corner10", valueType, Mutability.Const),
            FunctionArg("corner01", valueType, Mutability.Const),
            FunctionArg("corner11", valueType, Mutability.Const),
        ]

        if valueType.isScalar:
            weightType = VectorType((2,), valueType)
        else:
            assert valueType.isVector
            weightType = VectorType((2,), valueType.elementType)
        arguments.append(FunctionArg("weight", weightType, Mutability.Const))

        bilinearInterpolationOps.append(FunctionInterface(arguments=arguments, returnType=valueType,))

    trilinearInterpolationOps = []
    for valueType in [ScalarType(FLOAT)] + MATRIX_TYPES + SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        arguments = [
            FunctionArg("corner000", valueType, Mutability.Const),
            FunctionArg("corner100", valueType, Mutability.Const),
            FunctionArg("corner010", valueType, Mutability.Const),
            FunctionArg("corner110", valueType, Mutability.Const),
            FunctionArg("corner001", valueType, Mutability.Const),
            FunctionArg("corner101", valueType, Mutability.Const),
            FunctionArg("corner011", valueType, Mutability.Const),
            FunctionArg("corner111", valueType, Mutability.Const),
        ]

        if valueType.isScalar:
            weightType = VectorType((3,), valueType)
        else:
            assert valueType.isVector
            weightType = VectorType((3,), valueType.elementType)
        arguments.append(FunctionArg("weight", weightType, Mutability.Const))

        trilinearInterpolationOps.append(FunctionInterface(arguments=arguments, returnType=valueType,))

    # Map operators.
    mapOps = []
    for valueType in [ScalarType(FLOAT)] + MATRIX_TYPES + SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        if valueType.isScalar:
            rangeValueType = RangeType(valueType)
        else:
            assert valueType.isVector
            rangeValueType = RangeType(valueType.elementType)

        arguments = [
            FunctionArg("sourceValue", valueType, Mutability.Const),
            FunctionArg("sourceRange", rangeValueType, Mutability.Const),
            FunctionArg("targetRange", rangeValueType, Mutability.Const),
        ]

        mapOps.append(FunctionInterface(arguments=arguments, returnType=valueType,))

    # Map operators.
    clampOps = []
    for valueType in NUMERIC_SCALAR_TYPES + VECTOR_TYPES:
        if valueType.isScalar:
            rangeValueType = RangeType(valueType)
        else:
            assert valueType.isVector
            rangeValueType = RangeType(valueType.elementType)

        arguments = [
            FunctionArg("value", valueType, Mutability.Const),
            FunctionArg("range", rangeValueType, Mutability.Const),
        ]

        clampOps.append(FunctionInterface(arguments=arguments, returnType=valueType,))

    rayOps = []
    for valueType in (
        VectorType((2,), ScalarType(FLOAT)),
        VectorType((3,), ScalarType(FLOAT)),
    ):
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

    rangeOps = []
    for valueType in RANGE_TYPES:
        rangeOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", valueType, Mutability.Const),
                    FunctionArg("rhs", valueType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    expandOps = []
    for valueType in RANGE_TYPES:
        expandOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", valueType, Mutability.Const),
                    FunctionArg("rhs", valueType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )
        expandOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("lhs", valueType, Mutability.Const),
                    FunctionArg("rhs", valueType.elementType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    containerOps = []
    for valueType in RANGE_TYPES:
        # Element in container test.
        containerOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("container", valueType, Mutability.Const),
                    FunctionArg("containee", valueType.elementType, Mutability.Const),
                ],
                returnType=ScalarType(BOOL),
            )
        )

        # Container in container test.
        containerOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("container", valueType, Mutability.Const),
                    FunctionArg("containee", valueType, Mutability.Const),
                ],
                returnType=ScalarType(BOOL),
            )
        )

    quadraticOps = []
    for valueType in (ScalarType(FLOAT),):
        quadraticOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("a", valueType, Mutability.Const),
                    FunctionArg("b", valueType, Mutability.Const),
                    FunctionArg("c", valueType, Mutability.Const),
                    FunctionArg("roots", VectorType((2,), valueType), Mutability.Mutable),
                ],
                returnType=ScalarType(INT),
            )
        )

    raySphereIntersectionOps = []
    for valueType in (VectorType((3,), ScalarType(FLOAT)),):
        raySphereIntersectionOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("sphereOrigin", valueType, Mutability.Const),
                    FunctionArg("sphereRadius", valueType.elementType, Mutability.Const),
                    FunctionArg("rayOrigin", valueType, Mutability.Const),
                    FunctionArg("rayDirection", valueType, Mutability.Const),
                    FunctionArg("intersections", RangeType(valueType.elementType), Mutability.Mutable,),
                ],
                returnType=ScalarType(INT),
            )
        )

    rayAABBIntersectionOps = []
    for valueType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        rayAABBIntersectionOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("rayOrigin", valueType, Mutability.Const),
                    FunctionArg("rayDirection", valueType, Mutability.Const),
                    FunctionArg("aabb", RangeType(valueType), Mutability.Const),
                    FunctionArg("intersections", RangeType(valueType.elementType), Mutability.Mutable,),
                ],
                returnType=ScalarType(BOOL),
            )
        )

    # Random number generation.
    randomOps = []
    for valueType in NUMERIC_SCALAR_TYPES:
        randomOps.append(
            FunctionInterface(
                arguments=[FunctionArg("range", RangeType(valueType), Mutability.Const),], returnType=valueType,
            )
        )

    # Longest axis
    longestAxisOps = []
    for valueType in RANGE_TYPES_VECTOR:
        longestAxisOps.append(
            FunctionInterface(
                arguments=[FunctionArg("range", valueType, Mutability.Const),], returnType=ScalarType(INT),
            )
        )

    # Face forward
    faceForwardOps = []
    for valueType in SINGLE_INDEX_VECTOR_TYPES_FLOAT:
        faceForwardOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("normal", valueType, Mutability.Const),
                    FunctionArg("guide", valueType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    # Transform vector.
    transformVectorOps = []
    for matrixType in MATRIX_TYPES:
        vectorType = VectorType((matrixType.shape[0] - 1,), ScalarType(FLOAT))
        transformVectorOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("matrix", matrixType, Mutability.Const),
                    FunctionArg("vector", vectorType, Mutability.Const),
                ],
                returnType=vectorType,
            )
        )

    # Transform point.
    transformPointOps = []
    for valueType in (VectorType((3,), ScalarType(FLOAT)),):
        transformPointOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("matrix", VectorType((4, 4), ScalarType(FLOAT)), Mutability.Const),
                    FunctionArg("point", valueType, Mutability.Const),
                ],
                returnType=valueType,
            )
        )

    # Transform aabb.
    transformAABBOps = []
    for matrixType in (VectorType((4,4), ScalarType(FLOAT)),):
        vectorType = VectorType((matrixType.shape[0] - 1,), ScalarType(FLOAT))
        rangeType = RangeType(vectorType)
        transformAABBOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("matrix", matrixType, Mutability.Const),
                    FunctionArg("aabb", rangeType, Mutability.Const),
                ],
                returnType=rangeType,
            )
        )

    # Look at.
    lookAtOps = []
    for valueType in (VectorType((3,), ScalarType(FLOAT)),):
        lookAtOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("position", valueType, Mutability.Const),
                    FunctionArg("look", valueType, Mutability.Const),
                    FunctionArg("up", valueType, Mutability.Const),
                ],
                returnType=VectorType((4, 4), ScalarType(FLOAT)),
            )
        )

    # Matrix inverse.
    matrixInverseOps = []
    for valueType in (VectorType((4,4), ScalarType(FLOAT)),):
        matrixInverseOps.append(
            FunctionInterface(
                arguments=[
                    FunctionArg("matrix", valueType, Mutability.Const),
                    FunctionArg("inverse", valueType, Mutability.Mutable),
                ],
                returnType=ScalarType(BOOL),
            )
        )

    orthographicProjectionOps = [
        FunctionInterface(
            arguments=[
                FunctionArg("left", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("right", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("bottom", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("top", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("near", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("far", ScalarType(FLOAT), Mutability.Const),
            ],
            returnType=VectorType((4, 4), ScalarType(FLOAT)),
        )
    ]

    perspectiveProjectionOps = [
        # Frustum based.
        FunctionInterface(
            arguments=[
                FunctionArg("left", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("right", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("bottom", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("top", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("near", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("far", ScalarType(FLOAT), Mutability.Const),
            ],
            returnType=VectorType((4, 4), ScalarType(FLOAT)),
        ),
        # FOV and aspect ratio based.
        FunctionInterface(
            arguments=[
                FunctionArg("fieldOfView", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("aspectRatio", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("near", ScalarType(FLOAT), Mutability.Const),
                FunctionArg("far", ScalarType(FLOAT), Mutability.Const),
            ],
            returnType=VectorType((4, 4), ScalarType(FLOAT)),
        )
    ]

    viewportTransformOps = [
        FunctionInterface(
            arguments=[
                FunctionArg("dimensions", VectorType((2,), ScalarType(FLOAT)), Mutability.Const),
                FunctionArg("offset", VectorType((2,), ScalarType(FLOAT)), Mutability.Const),
            ],
            returnType=VectorType((4, 4), ScalarType(FLOAT)),
        )
    ]

    functionGroups = [
        # Basic.
        FunctionGroup(["floor", "ceil", "abs",], unaryOps, FunctionCategory.BASIC),
        FunctionGroup(["content",], rangeUnaryOps, FunctionCategory.BASIC),
        FunctionGroup(["min", "max",], binaryComparisonOps, FunctionCategory.BASIC),
        FunctionGroup(["quadraticRoots",], quadraticOps, FunctionCategory.BASIC),
        FunctionGroup(["degrees", "radians",], angleOps, FunctionCategory.BASIC),
        FunctionGroup(["randomNumber",], randomOps, FunctionCategory.BASIC),
        FunctionGroup(["linearInterpolation",], linearInterpolationOps, FunctionCategory.BASIC),
        FunctionGroup(["bilinearInterpolation",], bilinearInterpolationOps, FunctionCategory.BASIC),
        FunctionGroup(["trilinearInterpolation",], trilinearInterpolationOps, FunctionCategory.BASIC),
        FunctionGroup(["linearMap",], mapOps, FunctionCategory.BASIC),
        FunctionGroup(["clamp",], clampOps, FunctionCategory.BASIC),
        FunctionGroup(["intersection",], rangeOps, FunctionCategory.BASIC),
        FunctionGroup(["expand",], expandOps, FunctionCategory.BASIC),
        FunctionGroup(["contains"], containerOps, FunctionCategory.BASIC),
        FunctionGroup(["longestAxis"], longestAxisOps, FunctionCategory.BASIC),
        # Linear algebra.
        FunctionGroup(["isIdentity", "hasScale",], checkMatrixOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["setIdentity"], setMatrixOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["transpose"], matrixUnaryOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["matrixProduct"], matrixBinaryOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["normalize",], vectorOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["length", "lengthSquared",], vectorReductionOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["dotProduct",], vectorProductOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["crossProduct",], crossProductOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["distance"], pointReductionOps, FunctionCategory.LINEAR_ALGEBRA),
        FunctionGroup(["setTranslate", "setScale",], setVectorTransformOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["setRotateX", "setRotateY", "setRotateZ",], setRotateXYZOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["setRotate",], setRotateOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["coordinateSystem",], coordSysOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["faceForward",], faceForwardOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["transformVector",], transformVectorOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["transformPoint",], transformPointOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["transformAABB",], transformAABBOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["lookAt",], lookAtOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["inverse",], matrixInverseOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["orthographicProjection",], orthographicProjectionOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["perspectiveProjection",], perspectiveProjectionOps, FunctionCategory.LINEAR_ALGEBRA,),
        FunctionGroup(["viewportTransform",], viewportTransformOps, FunctionCategory.LINEAR_ALGEBRA,),
        # Ray tracing
        FunctionGroup(["rayPosition",], rayOps, FunctionCategory.RAY_TRACING),
        FunctionGroup(["raySphereIntersection",], raySphereIntersectionOps, FunctionCategory.RAY_TRACING,),
        FunctionGroup(["rayAABBIntersection",], rayAABBIntersectionOps, FunctionCategory.RAY_TRACING,),
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
            testTemplatePath = os.path.join(FUNCTIONS_DIR, TESTS_DIR, "test{name}.cpp".format(name=function.name))
            if os.path.isfile(GetTemplateFile(testTemplatePath)):
                filePaths.append(
                    GenerateCode(
                        testTemplatePath,
                        os.path.join(FUNCTIONS_DIR, TESTS_DIR, "test{name}.cpp".format(name=function.name),),
                        function=function,
                    )
                )

            # Benchmarking.
            filePaths.append(
                GenerateCode(
                    os.path.join(FUNCTIONS_DIR, BENCHMARKS_DIR, "benchmarkFunction.cpp"),
                    os.path.join(FUNCTIONS_DIR, BENCHMARKS_DIR, "benchmark{name}.cpp".format(name=function.name),),
                    function=function,
                )
            )

            # Python bindings source.
            filePaths.append(
                GenerateCode(
                    os.path.join(PYTHON_DIR, FUNCTIONS_DIR, "bindFunction.cpp"),
                    os.path.join(PYTHON_DIR, FUNCTIONS_DIR, "bind{name}.cpp".format(name=function.name),),
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
    parser = argparse.ArgumentParser("GraphicsMath code generation tool.")
    parser.add_argument(
        "-v",
        "--verbose",
        help="Set the logging level to DEBUG, producing more verbose outputs.",
        action="store_true",
    )

    args = parser.parse_args()
    if args.verbose:
        SetupLogging(logging.DEBUG)
    else:
        SetupLogging()

    # Generate the complete set ValueTypes first, pre-requisite to generating functions.
    filePaths, valueTypes = GenerateTypes()

    # Follow up with generating functions.
    filePaths += GenerateFunctions()

    # Generate python module.
    PrintMessage("Generating python module...")
    filePaths.append(
        GenerateCode(
            os.path.join(PYTHON_DIR, "module.cpp"),
            os.path.join(PYTHON_DIR, "module.cpp"),
            types=valueTypes,
            functions=FUNCTIONS.values(),
            UpperCamelCase=UpperCamelCase,
        )
    )
