""" submodel-python version """

from importlib.metadata import PackageNotFoundError, version


def get_version():
    """ Get the version of submodel-python """ ""
    try:
        return version("submodel")
    except PackageNotFoundError:
        return "unknown"


__version__ = get_version()