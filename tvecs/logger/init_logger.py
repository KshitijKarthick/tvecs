"""Initialise logging functionality."""
import sys
import logging


def initialise(handler_name):
    """
    Initialise the logger based on user preference.

    API Documentation
        :param handler_name: Handler name specified for logger.
        :type handler_name: :class:`String`
        :rtype: :class:`logging.Logger`

    .. seealso::
        * :mod:`logging`
    """
    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
    )
    logger = logging.getLogger(handler_name)
    return logger


def set_logger_level(level, logger):
    """
    Set Logging Level for specified logger.

    API Documentation
        :param level: Minimum level specified which can be logged.
        :param logger: Logger for which the level should be specified.
        :type level: :class:`Integer`
        :type logger: :class:`logging.Logger`
    """
    logger.setLevel(level)


def set_logger_verbose(logger):
    """
    Set Logger to verbose level.

    API Documentation
        :param logger: Logger for which the level should be specified.
        :type logger: :class:`logging.Logger`
    """
    set_logger_level(logging.DEBUG, logger)


def set_logger_silent(logger):
    """
    Set Logger to silent level.

    API Documentation
        :param logger: Logger for which the level should be specified.
        :type logger: :class:`logging.Logger`
    """
    set_logger_level(logging.ERROR, logger)


def set_logger_normal(logger):
    """
    Set Logger to info level.

    API Documentation
        :param logger: Logger for which the level should be specified.
        :type logger: :class:`logging.Logger`
    """
    set_logger_level(logging.INFO, logger)
