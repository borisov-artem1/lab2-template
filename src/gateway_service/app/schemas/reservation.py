from pydantic import BaseModel, constr, conint
from datetime import datetime as dt
from uuid import UUID

from enums.status import ReservationStatus
from schemas.library import LibraryResponse
from schemas.library import BookResponse


class ReservationBase(BaseModel):
  username: constr(max_length=80)
  bookUid: UUID
  libraryUid: UUID
  status: ReservationStatus
  startDate: dt
  tillDate: dt


class Reservation(ReservationBase):
  reservationUid: UUID


class BookReservationResponse(BaseModel):
  reservationUid: UUID
  username: constr(max_length=80)
  status: ReservationStatus
  startDate: dt
  tillDate: dt
  library: LibraryResponse
  book: BookResponse
