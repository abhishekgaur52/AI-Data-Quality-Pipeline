import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)

def log(msg):

    logging.info(msg)

    print(msg)

def log_error(e):

    logging.exception(e)