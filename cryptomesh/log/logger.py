import logging
from cryptomesh.log import Log
from cryptomesh import config

CRYPTOMESH_DEBUG  = config.CRYPTOMESH_DEBUG 

def console_handler_filter(record: logging.LogRecord):
    if CRYPTOMESH_DEBUG :
        return True
    return record.levelno in (logging.INFO, logging.WARNING, logging.ERROR)

def get_logger(name: str):
    return Log(
        name=name,
        console_handler_filter=console_handler_filter
    )

# Logger global opcional
L = get_logger("cryptomesh") 