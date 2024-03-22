import logging
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def setup_logger():
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(f'[%(time)s] {Fore.LIGHTBLACK_EX}~{Style.RESET_ALL} %(levelname)s {Fore.LIGHTBLACK_EX}~{Style.RESET_ALL} %(message)s')

    # Add color to the time part
    class ColorFormatter(logging.Formatter):
        def format(self, record):
            if record.levelname == 'INFO':
                record.levelname = f"{Fore.LIGHTBLUE_EX}{record.levelname}{Style.RESET_ALL}"
            elif record.levelname == 'WARNING':
                record.levelname = f"{Fore.YELLOW}{record.levelname}{Style.RESET_ALL}"
            elif record.levelname == 'ERROR':
                record.levelname = f"{Fore.RED}{record.levelname}{Style.RESET_ALL}"
            elif record.levelname == 'CRITICAL':
                record.levelname = f"{Fore.LIGHTRED_EX}{record.levelname}{Style.RESET_ALL}"
            record.time = f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}"
            return super().format(record)

    formatter = ColorFormatter(formatter._fmt)

    # Set formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to the logger
    logger.addHandler(console_handler)

    return logger

def main():
    logger = setup_logger()

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == "__main__":
    main()
