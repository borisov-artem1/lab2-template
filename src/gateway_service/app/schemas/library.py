from pydantic import BaseModel, conint, constr
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


class Library(LibraryBase):
  id: int
  library_uid: UUID


class LibraryResponse(LibraryBase):
  libraryUid: UUID


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


class Book(BookBase):
  id: int
  bookUid: UUID


class BookResponse(BookBase):
  bookUid: UUID


class BookPaginationResponse(BaseModel):
  page: conint(ge=1)
  pageSize: conint(ge=1)
  totalElements: conint(ge=0)
  items: list[BookResponse]


# ===== LibraryBookEntity =====
class LibraryBookEntityBase(BaseModel):
  libraryId: int
  bookId: int
  available_count: int


class LibraryBookEntity(LibraryBookEntityBase):
    id: int


class LibraryBookEntityResponse(LibraryBookEntityBase):
  id: int
  library: LibraryResponse
  book: BookResponse



# ===== LibraryBook =====
class LibraryBookResponse(BookBase):
  bookUid: UUID
  availableCount: int


class LibraryBookPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: list[LibraryBookResponse]
