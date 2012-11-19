__author__ = "Mapkin <opensource@mapkin.co>"
__version__ = '1.0.0'

__all__ = [
    'compress',
    'decompress',
]


try:
    from polycomp.speedups import (
        decompress,
        compress,
    )
except:
    from polycomp.codec import (
        decompress,
        compress,
    )
