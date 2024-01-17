from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class RespEnum(Enum):
    GetAllLibraries = {
        "description": "Все библиотеки в городе",
    }
    GetAllBooksInLibrary = {
        "description": "Все кники в библиотеке по uid",
    }
    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Ошибка валидации данных",
    }
