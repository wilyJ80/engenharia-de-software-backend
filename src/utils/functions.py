import os
import sys

def print_error_details(error: Exception) -> None:
    """
    Print error details

    Parameters
    ----------
    error : Exception
        Error to print details

    Notes
    -----
    Prints the error class, cause, type, filename, and line number of the error.

    Examples
    --------
    >>> print_error_details(error)
    error class: <class 'Exception'> | error cause: None
    <class 'Exception'> example.py 5
    """
    print(f'error class: {error.__class__} | error cause: {error.__cause__}')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

