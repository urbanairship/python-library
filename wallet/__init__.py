"""
    Python package for using the Urban Airship Wallet API
"""

from .wallet import *

from .template import *
from .pass_ import *
from .field import *
from .location import *
from .project import *
from .wict import *

from .wallet_iterable import (
    ProjectIterable,
    TemplateIterable,
    PassIterable,
)

from .convenience import *

try:
    from .internal import *
except ImportError:
    pass

# Silence urllib3 INFO logging by default

import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
