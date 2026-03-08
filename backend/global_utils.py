from jose import JWTError, jwt
from datetime import datetime, timedelta


def success_response(status_code: str, details: str, data=None):
    response = {"success": True, "status_code": status_code, "details": details}
    if data:
        response["data"] = data
    return response


class CustomException(Exception):
    def __init__(self, status_code, detail, error=None, trace_back=None, success=False):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.error = error
        self.trace_back = trace_back
        self.success = success


SECRET_KEY = "12346789JWT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def generate_token(data: dict):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
