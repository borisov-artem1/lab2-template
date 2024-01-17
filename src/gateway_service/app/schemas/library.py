from pydantic import BaseModel, constr
from uuid import UUID

from enums.status import ConditionStatus


# ======= Library =======
class LibraryBase(BaseModel):
  name: constr(max_length=80)
  city: constr(max_length=255)
  address: constr(max_length=255)


class LibraryFilter(BaseModel):
  name: constr(max_length=80) | None = None
  city: constr(max_length=255) | None = None
  address: constr(max_length=255) | None = None
  

class LibraryUpdate(BaseModel):
  name: constr(max_length=80) | None = None
  city: constr(max_length=255) | None = None
  address: constr(max_length=255) | None = None


class LibraryCreate(LibraryBase):
  name: constr(max_length=80) | None = None
  city: constr(max_length=255) | None = None
  address: constr(max_length=255) | None = None


class Library(LibraryBase):
  id: int
  library_uid: UUID


class LibraryResponse(LibraryBase):
  library_uid: UUID


class LibraryPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: list[LibraryResponse]


# ======= Book =======
class BookBase(BaseModel):
  name: constr(max_length=255)
  author: constr(max_length=255)
  genre: constr(max_length=255)
  condition: ConditionStatus


class BookFilter(BaseModel):
  name: constr(max_length=255) | None = None
  author: constr(max_length=255) | None = None
  genre: constr(max_length=255) | None = None
  condition: ConditionStatus | None = None
  

class BookUpdate(BaseModel):
  name: constr(max_length=255) | None = None
  author: constr(max_length=255) | None = None
  genre: constr(max_length=255) | None = None
  condition: ConditionStatus | None = None


class BookCreate(BookBase):
  condition: ConditionStatus = "EXCELLENT"


class Book(BookBase):
  id: int
  book_uid: UUID


# class LibraryResponse(LibraryBase):
#   library_uid: UUID


# class LibraryPaginationResponse():
#   page: int
#   pageSize: int
#   totalElemnts: int
#   items: list[LibraryResponse]




