"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def _parse_ratelimit_header(request):
    now = parsedate_to_datetime(request.headers.get('Date'))
    reset = datetime.fromtimestamp(int(request.headers.get('X-RateLimit-Reset')) / 1000, timezone.utc)
    return (reset - now).total_seconds()


class MaybeUnlock:
    def __init__(self, lock):
        self.lock = lock
        self._unlock = True

    def __enter__(self):
        return self

    def defer(self):
        self._unlock = False

    def __exit__(self, type, value , tb):
        if self._unlock:
            self.lock.release()
