import sys

from loguru import logger

_logger_id = 0


def configure_logger(debug: bool = False) -> None:
    """Configure the logger.

    Args:
        debug: Whether to set the logger level to DEBUG. Otherwise level is set to INFO.

    The logger is configured to print messages in the format: <level>{message}</level>
    """
    global _logger_id
    logger.remove(_logger_id)

    if debug:
        level = "DEBUG"
    else:
        level = "INFO"

    # format="<level>{time:HH:mm:ss.SS}</level> | <level>{level: <8}</level> | <level>{message}</level>", level=level)
    # logger.level("INFO", color="<green>")

    _logger_id = logger.add(sys.stdout, colorize=True, format="<level>{message}</level>", level=level)
