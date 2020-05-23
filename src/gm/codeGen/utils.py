"""
Common code generation utilities.
"""

import os
import shlex
import subprocess
import math

from jinja2 import Template

# Name of the codegen template directory.
TEMPLATE_DIR = "template"

# Python source file extension.
PY_SOURCE_EXT = ".py"

# CPP file extension(s).
CPP_SOURCE_EXT = ".cpp"
CPP_HEADER_EXT = ".h"


def GetFileExt(filePath):
    """
    Get the file extension of ``filePath``.
    """
    return os.path.splitext(filePath)[1]


def UpperCamelCase(lowerCamelCaseStr):
    """
    Return the UpperCamelCase variant of a lower camel case string.
    """
    return lowerCamelCaseStr[0].upper() + lowerCamelCaseStr[1:]


def LowerCamelCase(upperCamelCaseStr):
    """
    Return the lowerCamelCase variant of an upper camel case string.
    """
    return upperCamelCaseStr[0].lower() + upperCamelCaseStr[1:]


def RunCommand(command):
    """
    Run the ``command`` by forking a subprocess.
    """
    print("Running command {}".format(command))
    process = subprocess.Popen(shlex.split(command))
    process.wait()


def WriteFile(filePath, content):
    """
    Write a file to disk with ``content`` at the specified ``filePath``.

    Args:
        filePath (str): path to write to.
        content (str): content to write.
    """
    print("Generated {!r}".format(filePath))
    with open(filePath, "w") as f:
        f.write(content)


def FormatCode(fileNames):
    """
    Run clang-format over input files, formatting in-place.

    Args:
        fileNames (list): input files to automatically format.
    """
    pythonFiles = [fileName for fileName in fileNames if GetFileExt(fileName) == PY_SOURCE_EXT]
    if pythonFiles:
        RunCommand("black " + " ".join(pythonFiles))

    cppFiles = [fileName for fileName in fileNames
                if GetFileExt(fileName) in (CPP_SOURCE_EXT, CPP_HEADER_EXT)]
    if cppFiles:
        RunCommand("clang-format -i " + " ".join(cppFiles))


def GetTemplateFile(templateName):
    """
    Args:
        templateName (str): name of the template file.

    Returns:
        str: full path to the codegen template.
    """
    return os.path.abspath(os.path.join(TEMPLATE_DIR, templateName))


def GenerateCode(templatePath, **kwargs):
    """
    Generate a single source file with a template and code-gen context.

    Args:
        templatePath (str): path to the template file to perform substitution.

    Returns:
        str: file name of generated source file.
    """
    fileExt = GetFileExt(templatePath);
    if fileExt in (CPP_SOURCE_EXT, CPP_HEADER_EXT):
        commentPrefix = "//"
    elif fileExt == PY_SOURCE_EXT:
        commentPrefix = "#"
    else:
        raise ValueError("Unknown codegen template suffix: %s".format(fileExt))

    with open(templatePath, "r") as f:
        templateStr = f.read()
        templateStr = os.linesep.join(
            [
                commentPrefix,
                commentPrefix + " This file is auto-generated, please do not modify directly!",
                commentPrefix,
                "",
            ]
            + templateStr.split(os.linesep)
        )
        template = Template(templateStr)
        code = template.render(math=math, **kwargs)
        return code
