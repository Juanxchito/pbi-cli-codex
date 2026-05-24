"""pbi-cli: CLI for Power BI semantic models via direct .NET interop."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

try:
    __version__ = _pkg_version("pbi-cli-tool")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
