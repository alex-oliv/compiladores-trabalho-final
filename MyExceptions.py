class Error(Exception):
    pass


class DeclarationError(Error):
    pass


class OperationError(Error):
    pass


class MissingStatementError(Error):
    pass
