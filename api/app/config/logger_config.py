import logging


def get_logger(name: str, level: str = logging.INFO):
    strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=level,
        datefmt=datefmt,
        format=strfmt
    )

    logger = logging.getLogger(name)
    return logger
