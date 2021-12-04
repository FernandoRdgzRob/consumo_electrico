class UserNotFound(Exception):
    def __init__(self, message="User not found", details="No details provided"):
        self.message = f"Error: {message} > Details: {details}"
        super().__init__(self.message)
