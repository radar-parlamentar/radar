import logging

logger = logging.getLogger("radar")

class ExceptionLoggingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before the view
        response = self.get_response(request)
        # after the view
        return response

    """Sending log to the log file"""
    def process_exception(self, request, exception):
        logger.exception('Exception handling request for ' + request.path)
        return None
