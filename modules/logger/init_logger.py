"""Initialise logging functionality."""
import sys
import logging


def initialise(handler_name):
    """Initialise the logger based on user preference."""
    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
    )
    logger = logging.getLogger(handler_name)
    return logger


def set_logger_level(level, logger):
    """Set Logging Level for specified logger."""
    logger.setLevel(level)


def set_logger_verbose(logger):
    """Set Logger to verbose level."""
    set_logger_level(logging.DEBUG, logger)


def set_logger_silent(logger):
    """Set Logger to silent level."""
    set_logger_level(logging.ERROR, logger)


def set_logger_normal(logger):
    """Set Logger to info level."""
    set_logger_level(logging.INFO, logger)
