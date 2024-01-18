from pydantic import BaseModel, constr, conint, validator
from datetime import datetime
from uuid import UUID

from enums.status import ReservationStatus
from schemas.library import LibraryResponse, BookResponse
from schemas.rating import UserRatingResponse


def convert_datetime_to_iso_8601(dt: datetime) -> str:
  return dt.strftime('%Y-%m-%d')


class ReservationBase(BaseModel):
  username: constr(max_length=80)
  bookUid: UUID
  libraryUid: UUID
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime

  @validator("startDate", "tillDate", pre=True)
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)


class Reservation(ReservationBase):
  reservationUid: UUID


class ReservationCreate(BaseModel):
  username: constr(max_length=80)
  library_uid: UUID | str
  book_uid: UUID | str
  status: ReservationStatus
  start_date: datetime | str
  till_date: datetime | str

  @validator("start_date", "till_date", pre=True)
  def datetime_validate(cls, dt):
    return datetime.fromisoformat(dt)


class BookReservationResponse(BaseModel):
  reservationUid: UUID
  username: constr(max_length=80)
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime
  library: LibraryResponse
  book: BookResponse

  class Config:
    json_encoders = {
      datetime: convert_datetime_to_iso_8601
    }


class TakeBookRequest(BaseModel):
  libraryUid: UUID
  bookUid: UUID
  tillDate: datetime

  @validator("tillDate", pre=True)
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)
    

class TakeBookResponse(BaseModel):
  reservationUid: UUID
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime
  library: LibraryResponse
  book: BookResponse
  rating: UserRatingResponse

  class Config:
    json_encoders = {
      datetime: convert_datetime_to_iso_8601
    }
