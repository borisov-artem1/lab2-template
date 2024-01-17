from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class RespEnum(Enum):
    GetAllLibraries = {
        "description": "Все библиотеки в городе",
    }
    GetAllTickets = {
        "description": "Информация по всем билетам пользователя",
    }
    GetTicket = {
        "description": "Информация по конкретному билету",
    }
    BuyTicket = {
        "description": "Информация о купленном билете",
    }
    TicketRefund = {
        "description": "Возврат билета успешно выполнен",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    GetMe = {
        "description": "Полная информация о пользователе",
    }
    GetPrivilege = {
        "description": "Данные о бонусном счете",
    }

    FlightNumberNotFound = {
        "model": ErrorResponse,
        "description": "Рейс с таким номером не найден",
    }
    TicketNotFound = {
        "model": ErrorResponse,
        "description": "Билет не найден",
    }
    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Ошибка валидации данных",
    }
