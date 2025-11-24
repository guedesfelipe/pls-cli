try:
    from importlib.metadata import (
        version,  # type: ignore[no-redef] # Python 3.8+
    )
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]

__version__ = version('pls-cli')
