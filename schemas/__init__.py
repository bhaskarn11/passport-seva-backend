from fastapi import HTTPException


class CustomHTTPException(HTTPException):

    detail = {"message": "Internal Server Error Occurred"}

    def __init__(self, message: str, status_code: int = 500):
        self.detail = {"message": message}
        self.status_code = status_code
