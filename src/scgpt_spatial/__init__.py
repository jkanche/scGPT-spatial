import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "scgpt-spatial"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# __version__ = "0.1.0"
import logging
import sys

logger = logging.getLogger("scGPT-spatial")
from . import model, tokenizer, utils, tasks
from .data_collator import DataCollator
from .data_sampler import SubsetsBatchSampler
from .preprocess import *