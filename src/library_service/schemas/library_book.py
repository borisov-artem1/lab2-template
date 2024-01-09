from pydantic import BaseModel


class LibraryBookBase(BaseModel):
    library_id: int
    book_id: int
    available_count: int


class LibraryBookFilter(BaseModel):
    library_id: int | None = None
    book_id: int | None = None
    available_count: int | None = None


class PrivilegeHistoryCreate(LibraryBookBase):
    pass


class PrivilegeHistory(LibraryBookBase):
    id: int
