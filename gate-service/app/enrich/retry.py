import time

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import Timeout


RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


def retry(operation, attempts=3, delay=1):
    """
    Retry an operation using exponential backoff.

    delays:
        1
        2
        4
    """

    current_delay = delay

    for attempt in range(attempts):

        try:
            return operation()

        except HTTPError as exc:

            status = exc.response.status_code

            if (
                status not in RETRYABLE_STATUS_CODES
                or attempt == attempts - 1
            ):
                raise

        except (Timeout, ConnectionError):

            if attempt == attempts - 1:
                raise

        time.sleep(current_delay)

        current_delay *= 2