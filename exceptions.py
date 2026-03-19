class DuplicateEmailError(Exception):
    """
    Raised when trying to create a user with an email that already exists in the DB.
    
    Caught by the router → returned as 409 Conflict
    """
    pass


class UserNotFoundError(Exception):
    """
    Raised when a user lookup by ID returns no result.
    
    Caught by the router → returned as 404 Not Found
    """
    pass