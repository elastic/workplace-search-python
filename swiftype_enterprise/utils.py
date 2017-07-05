import signal
import platform
from functools import wraps
from .exceptions import SynchronousDocumentIndexingFailed

class Timeout:

    def __init__(self, exception_class, seconds=1, error_message='Timeout'):
        self.exception_class = exception_class
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise self.exception_class(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

def windows_incompatible(error_message=None):
    error_message = error_message or 'This function is not supported on Windows.'

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if platform.system() == 'Windows':
                raise OSError(error_message)
            return f(*args, **kwargs)
        return decorated

    return decorator
