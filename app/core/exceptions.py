from fastapi import HTTPException


class UniqueException(HTTPException):
    def __init__(self, field: str):
        super().__init__(status_code=400, detail=f"{field} already exists")
        self.field = field
