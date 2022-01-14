import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    format="%(message)s"
)

for handler in logging.root.handlers:
    handler.terminator = ""


def get_logger() -> logging.Logger:
    return logging.getLogger("python-progress")
