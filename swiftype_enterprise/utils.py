import signal
import platform
from functools import wraps
from .exceptions import SynchronousDocumentIndexingFailed

class Timeout:

    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise SynchronousDocumentIndexingFailed(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

def windows_incompatible(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if platform.system() == 'Windows':
            raise OSError('This function is not supported on Windows. '
                          'Please use `async_index_documents` instead.')
        return f(*args, **kwargs)

    return decorated