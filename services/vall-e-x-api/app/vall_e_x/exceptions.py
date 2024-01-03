from ..exceptions import ApplicationException

class DetectedTextNotFoundException(ApplicationException):
    """Exception raised when detected text is not found"""
    def __init__(self):
        super().__init__("DetectedText not found", 500)