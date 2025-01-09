class CustomError(Exception):
    def __init__(self, message="Error"):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(CustomError):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

class ValidationError(CustomError):
    def __init__(self, message="Invalid input"):
        self.message = message
        super().__init__(self.message)

class DatabaseError(CustomError):
    def __init__(self, message="Database Error"):
        self.message = message
        super().__init__(self.message)