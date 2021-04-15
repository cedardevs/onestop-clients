import logging


class ClientLogger:
    """
    Logging class utilizing python logging library

    Methods
    -------
    get_logger(log_name, log_level, create_file=False)
        creates a logger for debugging and info purposes

    """
    def get_logger(log_name, log_level, create_file=False):
        """

        :param log_name: str
            defined logging name
        :param log_level: str
            type of logging you want (DEBUG, INFO, etc)
        :param create_file: boolean
            defines whether or not you want a file to be created for the log statements

        :return: logging object
        """

        # create logger
        logger = logging.getLogger(log_name)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if log_level == "DEBUG":
            logger.setLevel(level=logging.DEBUG)
        else:
            if log_level == "INFO":
                logger.setLevel(level=logging.INFO)
            else:
                logger.setLevel(level=logging.ERROR)

        fh = None
        if create_file:
            # create file handler for logger.
            fh = logging.FileHandler(log_name)
            fh.setFormatter(formatter)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handlers to logger.
        if create_file:
            logger.addHandler(fh)

        logger.addHandler(ch)

        return logger
