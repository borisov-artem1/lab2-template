from uuid import UUID
import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings
from schemas.library import (
  LibraryResponse,
  BookResponse,
)


class LibraryCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    library_host = settings["services"]["gateway"]["library_host"]
    library_port = settings["services"]["library"]["port"]

    self.http_path = f'http://{library_host}:{library_port}/api/v1/'

  async def get_all_libraries(
      self,
      page: int = 1,
      size: int = 100,
      city: str | None = None,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}library/?page={page}&size={size}'\
        f'{f"&city={city}" if city else ""}'
    )
    self._check_status_code(response.status_code)
    
    return response.json()
  

  async def get_all_library_books(
      self,
      page: int = 1,
      size: int = 100,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}library_book/?page={page}&size={size}'
    )
    self._check_status_code(response.status_code)

    return response.json()
  

  async def get_library_by_uid(
      self,
      uid: UUID,
  ) -> LibraryResponse:
    response: Response = requests.get(
      url=f'{self.http_path}library/{uid}',
    )
    self._check_status_code(response.status_code)

    library_json = response.json()

    return LibraryResponse(
      libraryUid=library_json["library_uid"],
      name=library_json["name"],
      city=library_json["city"],
      address=library_json["address"],
    )
  

  async def get_book_by_uid(
      self,
      uid: UUID,
  ) -> BookResponse:
    response: Response = requests.get(
      url=f'{self.http_path}book/{uid}',
    )
    self._check_status_code(response.status_code)

    book_json = response.json()

    return BookResponse(
      bookUid=book_json["book_uid"],
      name=book_json["name"],
      author=book_json["author"],
      genre=book_json["genre"],
      condition=book_json["condition"],
    )
  
