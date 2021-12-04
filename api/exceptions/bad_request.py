class WrongData(Exception):
    def __init__(
        self,
        message="Data provided for request is incomplete or incorrect",
        details="No details provided",
    ):
        self.message = f"Error: {message} > Details: {details}"
        super().__init__(self.message)
