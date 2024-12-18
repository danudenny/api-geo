from typing import Optional, Any, Dict, TypeVar, Generic
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from http import HTTPStatus

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: bool
    message: str
    data: Optional[T] = None
    error: Optional[Dict[str, Any]] = None

class ResponseHelper:
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = HTTPStatus.OK) -> Dict[str, Any]:
        return {
            "status": True,
            "message": message,
            "data": data,
            "error": None
        }

    @staticmethod
    def error(message: str = "Error", error: Dict[str, Any] = None,
              status_code: int = HTTPStatus.BAD_REQUEST) -> Dict[str, Any]:
        return {
            "status": False,
            "message": message,
            "data": None,
            "error": error
        }

    @staticmethod
    def not_found(message: str = "Not Found", error: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "status": False,
            "message": message,
            "data": None,
            "error": error
        }

    @staticmethod
    def json_response(data: Dict[str, Any], status_code: int = HTTPStatus.OK) -> JSONResponse:
        return JSONResponse(
            content=data,
            status_code=status_code
        )
        return Response(success=False, message="Not Found", error=error)