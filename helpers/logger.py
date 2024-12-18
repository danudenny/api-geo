from loguru import logger

def log_success(message):
    logger.success(message)

def log_error(message):
    logger.error(message)


def log_warning(message):
    logger.warning(message)


def log_info(message):
    logger.info(message)


def log_debug(message):
    logger.debug(message)


def log_critical(message):
    logger.critical(message)


def log_exception(message):
    logger.exception(message)