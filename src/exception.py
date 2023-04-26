import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    # Get the details of the exception that was raised
    _,_,exc_tb=error_detail.exc_info() 

    # Extract the name of the Python script
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Format the details into a string and return the error message
    error_message = "Error occured in py script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno,str(error))

    return error_message
    

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        # Call the constructor of the base class to initialize the exception object
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        # Convert the exception object to a string representation
        return self.error_message
