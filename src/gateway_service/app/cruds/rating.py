import json
from uuid import UUID
import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings
from schemas.rating import Rating, RatingUpdate


class RatingCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    rating_host = settings["services"]["gateway"]["rating_host"]
    rating_port = settings["services"]["rating"]["port"]

    self.http_path = f'http://{rating_host}:{rating_port}/api/v1/'

  async def get_all_ratings(
      self,
      page: int = 1,
      size: int = 100,
      username: str | None = None,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}rating/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}'
    )
    self._check_status_code(response.status_code)

    rating_json: list[Rating] = response.json()

    ratings: list[Rating] = []
    for rating in rating_json:
      ratings.append(
        Rating(
          id=rating["id"],
          username=rating["username"],
          stars=rating["stars"],
        )
      )
    
    return ratings
  

  async def patch_rating(
      self,
      id: int,
      update: RatingUpdate,
  ):
    response: Response = requests.patch(
      url=f'{self.http_path}rating/{id}',
      data=json.dumps(update.model_dump(exclude_unset=True))
    )
    self._check_status_code(response.status_code)

    rating = response.json()
    return rating["id"]
