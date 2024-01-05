__author__ = "VadimTrubay"

from datetime import datetime


def log(message: str):
    """
    The log function takes a string as an argument and writes it to the logs.txt file with a timestamp.
    :param message: str: Specify the type of data that is expected to be passed into the function
    :return: Nothing, it just writes the message to a file
    """
    current_time = datetime.strftime(datetime.now(), "[%Y-%m-%d] [%H:%M:%S]")
    full_message = f"{current_time} - {message}"
    with open("logs.txt", "a") as file:
        file.write(f"{full_message}\n")
