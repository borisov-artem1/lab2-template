from pydantic import BaseModel, conint


class LibraryBookBase(BaseModel):
    library_id: int
    book_id: int
    available_count: int


class LibraryBookFilter(BaseModel):
    library_id: int | None = None
    book_id: int | None = None
    available_count: int | None = None


class LibraryBookUpdate(BaseModel):
    library_id: conint(ge=1) | None = None
    book_id: conint(ge=1) | None = None
    available_count: conint(ge=0) | None = None


class LibraryBookCreate(LibraryBookBase):
    pass


class LibraryBook(LibraryBookBase):
    id: int
