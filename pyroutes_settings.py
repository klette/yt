import os

TEMPLATE_DIR  = os.path.join(
    os.path.dirname(__file__),
    'templates'
    )

MP3_DIR = os.path.join(
    os.path.dirname(__file__),
    'media',
    'audio',
    )

DB_DSN = "host=localhost port=5433 dbname=yt user=yt password=foobar"

try:
    from local_config import *
except ImportError:
    pass
