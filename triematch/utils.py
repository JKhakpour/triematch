"""utility functions used in retire library."""
from collections.abc import Iterable
from itertools import tee
from sys import version_info

if version_info.minor > 9: #noqa PLR2004
    from itertools import pairwise
else:

    def pairwise(iterable: Iterable) -> Iterable:
        """
        Sequential pair of an iterator.

        pairwise('ABCDEFG') --> AB BC CD DE EF FG
        added for backward compatibilty with python 3.9
        """
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
