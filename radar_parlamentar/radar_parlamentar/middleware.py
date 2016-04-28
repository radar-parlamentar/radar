import logging
import re
from django.middleware.cache import UpdateCacheMiddleware


class ConsoleExceptionMiddleware:
    """Custom middleware to print stack traces on Django console"""

    def process_exception(self, request, exception):
        import traceback
        import sys
        exc_info = sys.exc_info()
        exception = traceback.format_exception(*(exc_info or sys.exc_info()))
        print "######################## Exception ###########################"
        print '\n'.join(exception)
        print "##############################################################"

logger = logging.getLogger("radar")


class ExceptionLoggingMiddleware(object):
    """Sending log to the log file"""
    def process_exception(self, request, exception):
        logger.exception('Exception handling request for ' + request.path)


class SmartUpdateCacheMiddleware(UpdateCacheMiddleware):
    STRIP_RE = re.compile(r'\b(_[^=]+=.+?(?:; |$))')

    def process_request(self, request):
        cookie = self.STRIP_RE.sub('', request.META.get('HTTP_COOKIE', ''))
        request.META['HTTP_COOKIE'] = cookie
