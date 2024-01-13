from sqlalchemy.orm import Session

from cruds.library_book import LibraryBookCRUD
from schemas.library_book import LibraryBookFilter, LibraryBookUpdate, LibraryBookCreate
from exceptions.http import NotFoundException, ConflictException
from models.library_book import LibraryBookModel


class LibraryBookService():
  def __init__(self, library_bookCRUD: LibraryBookCRUD, db: Session):
    self._library_bookCRUD: LibraryBookCRUD = library_bookCRUD(db)

  async def get_all(
      self,
      filter: LibraryBookFilter,
      page: int = 1,
      size: int = 100,
  ):
    return await self._library_bookCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
  
  async def get_by_id(
      self, 
      id: int,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="get library_book")
    
    return library_book

  async def create(
      self,
      library_book_create: LibraryBookCreate,
  ):
    library_book = LibraryBookModel(**library_book_create.model_dump())
    library_book = await self._library_bookCRUD.create(library_book)
    if library_book is None:
      raise ConflictException(prefix="create library_book")
    
    return library_book
  
  async def patch(
      self,
      id: int,
      library_book_patch: LibraryBookUpdate,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="patch library_book")
    
    library_book = await self._library_bookCRUD.update(library_book, library_book_patch)
    if library_book is None:
      raise ConflictException(prefix="patch library_book")
    
    return library_book
  
  async def delete(
      self,
      id: int,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="delete library_book")
    
    return await self._library_bookCRUD.delete(library_book)
