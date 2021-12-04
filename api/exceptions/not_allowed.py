class UserNotAllowed(Exception):
    def __init__(
        self,
        message="User not allowed to access resource",
        details="No details provided",
    ):
        self.message = f"Error: {message} > Details: {details}"
        super().__init__(self.message)
