from pydantic import BaseModel, constr, conint
from datetime import datetime as dt
from uuid import UUID

from enums.status import ReservationStatus


class ReservationBase(BaseModel):
    username: constr(max_length=80)
    library_uid: UUID
    book_uid: UUID
    status: ReservationStatus
    start_date: dt
    till_date: dt


class ReservationFilter(BaseModel):
    username: constr(max_length=80) | None = None
    library_uid: UUID | None = None
    book_uid: UUID | None = None
    status: ReservationStatus | None = None
    start_date: dt | None = None
    till_date: dt | None = None
    

class ReservationUpdate(BaseModel):
    username: constr(max_length=80) | None = None
    library_uid: UUID | None = None
    book_uid: UUID | None = None
    status: ReservationStatus | None = None
    start_date: dt | None = None
    till_date: dt | None = None


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    reservation_uid: UUID
    
