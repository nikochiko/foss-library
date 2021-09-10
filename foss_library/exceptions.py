import os

MAX_OUTSTANDING_DUES = int(os.getenv("MAX_OUTSTANDING_DUES", 500))


class FOSSLibraryBaseException(Exception):
    pass


class OutOfStockError(FOSSLibraryBaseException):
    def __init__(self, *args, **kwargs):
        if not args:
            # no args passed, add an error message to it
            args = ("This book is out of stock",)

        return super().__init__(*args, **kwargs)


class OutstandingDuesError(FOSSLibraryBaseException):
    def __init__(self, *args, **kwargs):
        if not args:
            # no args passed, add an error message to it
            args = (
                f"Member's outstanding dues exceed {MAX_OUTSTANDING_DUES},"
                " they are not allowed to issue new books without clearing"
                " the existing dues",
            )
