import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings


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
  
