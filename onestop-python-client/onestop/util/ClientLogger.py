import logging


class ClientLogger:

    @staticmethod
    def get_logger(self, log_name, log_level, create_file=False):

        # create logger
        logger = logging.getLogger(self.__class__.__name__)

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
